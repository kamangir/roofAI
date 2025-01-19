import os
from typing import List, Tuple
import numpy as np
from enum import Enum, auto

from blueness import module
from blue_options import string
from blue_objects import file, path, objects
from blue_objects.metadata import get_from_object
from blue_objects.storage import instance as storage

from roofai import NAME
from roofai.dataset.ingest.CamVid import CLASSES as CAMVID_CLASSES
from roofai.semseg import (
    chip_width as semseg_chip_width,
    chip_height as semseg_chip_height,
)
from roofai.dataset.sagemaker import (
    chip_width as sagesemseg_chip_width,
    chip_height as sagesemseg_chip_height,
)
from roofai.semseg.utils import visualize
from roofai.logger import logger

NAME = module.name(__file__, NAME)


class DatasetTarget(Enum):
    TORCH = auto()
    SAGEMAKER = auto()

    @property
    def chip_height(self) -> int:
        if self == DatasetTarget.TORCH:
            return semseg_chip_height

        assert self == DatasetTarget.SAGEMAKER
        return sagesemseg_chip_height

    @property
    def chip_width(self) -> int:
        if self == DatasetTarget.TORCH:
            return semseg_chip_width

        assert self == DatasetTarget.SAGEMAKER
        return sagesemseg_chip_width


class MatrixKind(Enum):
    IMAGE = auto()
    MASK = auto()

    def filename_and_extension(
        self,
        dataset_kind,
        subset,
        record_id,
    ):
        return "{}/{}.{}".format(
            self.subset_path(dataset_kind, subset),
            record_id,
            dataset_kind.file_extension(self),
        )

    def subset_path(
        self,
        dataset_kind,
        subset,
    ) -> str:
        sagemaker_val_adapter = lambda subset: (
            "validation" if subset == "val" else subset
        )

        return (
            (subset if self == MatrixKind.IMAGE else f"{subset}annot")
            if dataset_kind == DatasetKind.CAMVID
            else (
                (
                    sagemaker_val_adapter(subset)
                    if self == MatrixKind.IMAGE
                    else f"{sagemaker_val_adapter(subset)}_annotation"
                )
                if dataset_kind == DatasetKind.SAGEMAKER
                else (
                    f"{subset}/image" if self == MatrixKind.IMAGE else f"{subset}/label"
                )
            )
        )


class DatasetKind(Enum):
    AIRS = auto()
    CAMVID = auto()
    SAGEMAKER = auto()
    DISTRIBUTED = auto()

    def file_extension(self, kind: MatrixKind) -> str:
        if self in [DatasetKind.AIRS, DatasetKind.DISTRIBUTED]:
            return "tif"

        if self == DatasetKind.CAMVID:
            return "png"

        assert self == DatasetKind.SAGEMAKER
        if kind == MatrixKind.MASK:
            return "png"

        assert kind == MatrixKind.IMAGE
        return "jpg"

    @property
    def prefix_path(self) -> str:
        return "SegNet-Tutorial/CamVid/" if self == DatasetKind.CAMVID else ""


class RoofAIDataset:
    SUBSETS = "test,train,val".split(",")

    def __init__(self, dataset_path, kind=None):
        self.path = dataset_path
        self.object_name = path.name(self.path)

        _, self.metadata = file.load_yaml(
            os.path.join(self.path, "metadata.yaml"),
            ignore_error=True,
        )

        self.source = self.metadata.get("source", "AIRS")
        self.kind = DatasetKind[
            self.metadata.get(
                "kind",
                (
                    self.source
                    if kind is None
                    else kind.name if isinstance(kind, DatasetKind) else kind
                ),
            ).upper()
        ]

        if self.kind == DatasetKind.DISTRIBUTED:
            if self.metadata["datacube_id"]:
                datacube_id = self.metadata["datacube_id"][0]
                self.classes = get_from_object(
                    object_name=datacube_id,
                    key="rasterize",
                    default={},
                    download=True,
                ).get("list_of_classes", [])
            else:
                self.classes = []
        else:
            self.classes = self.metadata.get(
                "classes",
                "other,roof".split(",") if self.source == "AIRS" else CAMVID_CLASSES,
            )

        self.subsets = {
            subset: self.list_of_record_id(subset) for subset in self.SUBSETS
        }

        logger.info(self.one_liner)

    def create(self, log: bool = False):
        for subset in self.subsets:
            for matrix_kind in list(MatrixKind):
                path.create(
                    self.subset_path(subset, matrix_kind),
                    log=log,
                )
        return self

    def subset_path(
        self,
        subset: str,
        matrix_kind: MatrixKind,
    ) -> str:
        return os.path.join(
            self.dataset_path,
            matrix_kind.subset_path(self.kind, subset),
        )

    def list_of_record_id(
        self,
        subset: str,
        matrix_kind: MatrixKind = MatrixKind.IMAGE,
    ) -> List[str]:
        if self.kind == DatasetKind.DISTRIBUTED:
            return self.metadata.get("datacube_id", []) if subset == "train" else []

        return sorted(
            [
                file.name(filename)
                for filename in file.list_of(
                    os.path.join(
                        self.subset_path(subset, matrix_kind),
                        f"*.{self.kind.file_extension(matrix_kind)}",
                    )
                )
            ]
        )

    @property
    def one_liner(self) -> str:
        return "{}[kind:{},source:{}]({}): {} subset(s): {} - {} class(es): {}".format(
            self.__class__.__name__,
            self.kind,
            self.source,
            self.object_name,
            len(self.subsets),
            " + ".join(
                [
                    "{:,d} X {}".format(len(ids), subset)
                    for subset, ids in self.subsets.items()
                ]
            ),
            len(self.classes),
            ", ".join(self.classes),
        )

    @property
    def dataset_path(self) -> str:
        return os.path.join(self.path, self.kind.prefix_path)

    def get_filename(
        self,
        subset: str,
        record_id: str,
        matrix_kind: MatrixKind = MatrixKind.IMAGE,
        log: bool = False,
    ) -> str:
        assert isinstance(matrix_kind, MatrixKind)

        if self.kind == DatasetKind.DISTRIBUTED:
            record_metadata = get_from_object(
                object_name=record_id,
                key="rasterize",
                default={},
                download=True,
            )

            filename = record_metadata["reference_filename"]
            if matrix_kind == MatrixKind.MASK:
                filename = file.add_suffix(filename, "label")

            assert storage.download_file(f"bolt/{record_id}/{filename}", "object")

            filename = objects.path_of(filename, record_id)
        else:
            filename = os.path.join(
                self.dataset_path,
                matrix_kind.filename_and_extension(self.kind, subset, record_id),
            )

        if log:
            logger.info(
                "{}[{}].get_filename({},{},{}): {}".format(
                    self.__class__.__name__,
                    self.object_name,
                    subset,
                    record_id,
                    matrix_kind,
                    filename,
                )
            )

        return filename

    def get_matrix(
        self,
        subset: str,
        record_id: str,
        kind: MatrixKind = MatrixKind.IMAGE,
        log: bool = False,
    ):
        success, matrix = file.load_image(
            self.get_filename(subset, record_id, kind, log)
        )
        assert success

        unique_value = np.array([])
        if kind == MatrixKind.MASK:
            matrix = matrix[:, :, 0]
            unique_value = np.unique(matrix)

        if log:
            logger.info(
                "{}[{}].get_matrix({},{},{}): {}{}".format(
                    self.__class__.__name__,
                    self.object_name,
                    subset,
                    record_id,
                    kind,
                    string.pretty_shape_of_matrix(matrix),
                    (
                        "{} unique value(s): {}".format(
                            len(unique_value),
                            unique_value,
                        )
                        if kind == MatrixKind.MASK
                        else ""
                    ),
                )
            )

        return matrix

    def shape(
        self,
        subset: str = "train",
        index: int = 0,
        kind: MatrixKind = MatrixKind.IMAGE,
        log: bool = False,
    ):
        return self.get_matrix(
            subset=subset,
            record_id=self.subsets[subset][index],
            kind=kind,
            log=log,
        ).shape

    def visualize(
        self,
        subset: str,
        index: Tuple[int, str],
        filename: str = "auto",
        in_notebook: bool = False,
        description: List[str] = [],
        log: bool = False,
    ):
        if index >= len(self.subsets[subset]):
            logger.warning(
                "{}.visualize: item ignored, index={} > len(subset[{}]) = {}.".format(
                    NAME,
                    index,
                    subset,
                    len(self.subsets[subset]),
                )
            )
            return

        record_id = self.subsets[subset][index] if isinstance(index, int) else index
        logger.info("record_id: {}".format(record_id))

        image = self.get_matrix(
            subset,
            record_id,
            MatrixKind.IMAGE,
            log=log,
        )

        mask = self.get_matrix(
            subset,
            record_id,
            MatrixKind.MASK,
            log=log,
        )

        visualize(
            {
                "image": image,
                "mask": mask,
            },
            filename=(
                os.path.join(
                    self.path,
                    f"_review/{record_id}.png",
                )
                if filename == "auto"
                else filename
            ),
            in_notebook=in_notebook,
            description=[
                self.object_name,
                f"{subset}/#{index}:{record_id}",
                f"kind: {self.kind.name.lower()}",
            ]
            + description,
        )
