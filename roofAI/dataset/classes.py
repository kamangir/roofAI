import os
from enum import Enum, auto
from roofAI.dataset.ingest.CamVid import CLASSES as CAMVID_CLASSES
from typing import List, Tuple
import numpy as np
from abcli import path
from abcli import string
from abcli import file
from roofAI.semseg.utils import visualize
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class DatasetKind(Enum):
    AIRS = auto()
    CAMVID = auto()

    @property
    def file_extension(self):
        return "png" if self == DatasetKind.CAMVID else "tif"

    @property
    def prefix_path(self):
        return "SegNet-Tutorial/CamVid/" if self == DatasetKind.CAMVID else ""


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
            dataset_kind.file_extension,
        )

    def subset_path(
        self,
        dataset_kind,
        subset,
    ) -> str:
        return (
            (subset if self == MatrixKind.IMAGE else f"{subset}annot")
            if dataset_kind == DatasetKind.CAMVID
            else (f"{subset}/image" if self == MatrixKind.IMAGE else f"{subset}/label")
        )


class RoofAIDataset(object):
    SUBSETS = "test,train,val".split(",")

    def __init__(self, dataset_path, kind=None):
        self.path = dataset_path
        self.object_name = path.name(self.path)

        _, self.metadata = file.load_yaml(
            os.path.join(self.path, "metadata.yaml"),
            civilized=True,
        )

        self.source = self.metadata.get("source", "AIRS")
        self.kind = DatasetKind[
            self.metadata.get(
                "kind",
                self.source
                if kind is None
                else kind.name
                if isinstance(kind, DatasetKind)
                else kind,
            ).upper()
        ]

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
        return sorted(
            [
                file.name(filename)
                for filename in file.list_of(
                    os.path.join(
                        self.subset_path(subset, matrix_kind),
                        f"*.{self.kind.file_extension}",
                    )
                )
            ]
        )

    @property
    def one_liner(self):
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
    def dataset_path(self):
        return os.path.join(self.path, self.kind.prefix_path)

    def get_filename(
        self,
        subset: str,
        record_id: str,
        matrix_kind: MatrixKind = MatrixKind.IMAGE,
        log: bool = False,
    ):
        assert isinstance(matrix_kind, MatrixKind)
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
                    "{} unique value(s): {}".format(
                        len(unique_value),
                        unique_value,
                    )
                    if kind == MatrixKind.MASK
                    else "",
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
                "mask": mask / np.max(mask),
            },
            filename=os.path.join(
                self.path,
                f"_review/{record_id}.png",
            )
            if filename == "auto"
            else filename,
            in_notebook=in_notebook,
            description=[
                self.object_name,
                f"{subset}/#{index}:{record_id}",
            ]
            + description,
        )
