import os
from enum import Enum, auto
import numpy as np
from abcli import path
from abcli import string
from abcli import file
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class Kind(Enum):
    IMAGE = auto()
    MASK = auto()


class RoofAIDataset(object):
    def __init__(self, dataset_path):
        self.path = dataset_path
        self.object_name = path.name(self.path)

        success, self.metadata = file.load_yaml(
            os.path.join(self.path, "metadata.yaml")
        )
        assert success

        self.subsets = {
            subset: [
                file.name(filename)
                for filename in file.list_of(
                    os.path.join(self.dataset_path, subset, "*.png")
                )
            ]
            for subset in "test,train,val".split(",")
        }

        logger.info(self.one_liner)

    @property
    def one_liner(self):
        return "{}[{}]: {} subset(s): {}".format(
            self.__class__.__name__,
            self.object_name,
            len(self.subsets),
            " + ".join(
                [
                    "{:,d} X {}".format(len(ids), subset)
                    for subset, ids in self.subsets.items()
                ]
            ),
        )

    @property
    def dataset_path(self):
        return (
            os.path.join(self.path, "SegNet-Tutorial/CamVid/")
            if self.source == "CamVid"
            else self.path
        )

    def get_filename(
        self,
        subset: str,
        record_id: str,
        kind: Kind = Kind.IMAGE,
        log: bool = False,
    ):
        assert isinstance(kind, Kind)
        filename = (
            os.path.join(self.dataset_path, f"{subset}/{record_id}.png")
            if kind == Kind.IMAGE
            else os.path.join(self.dataset_path, f"{subset}annot/{record_id}.png")
        )

        if log:
            logger.info(
                "{}[{}].get_filename({},{},{}): {}".format(
                    self.__class__.__name__,
                    self.object_name,
                    subset,
                    record_id,
                    kind,
                    filename,
                )
            )

        return filename

    def get_matrix(
        self,
        subset: str,
        record_id: str,
        kind: Kind = Kind.IMAGE,
        log: bool = False,
    ):
        success, matrix = file.load_image(
            self.get_filename(subset, record_id, kind, log)
        )
        assert success

        if kind == Kind.MASK:
            matrix = matrix[:, :, 0]

            unique_value = np.unique(matrix)
            logger.info(
                "{} unique value(s): {}".format(
                    len(unique_value),
                    unique_value,
                )
            )

        if log:
            logger.info(
                "{}.get_matrix({},{},{}): {}".format(
                    self.__class__.__name__,
                    subset,
                    record_id,
                    kind,
                    string.pretty_shape_of_matrix(matrix),
                )
            )

        return matrix

    @property
    def source(self):
        return self.metadata.get("source", "unknown")
