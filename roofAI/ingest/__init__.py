import os
from enum import Enum, auto as auto_
from abcli import path


class DatasetSource(Enum):
    AIRS = auto_()
    AUTO = auto_()
    CAMVID = auto_()

    def adjust_path(self, object_path: str):
        dataset_source = (
            DatasetSource.auto(object_path) if self == DatasetSource.AUTO else self
        )

        if dataset_source == DatasetSource.CAMVID:
            object_path = os.path.join(object_path, "SegNet-Tutorial/CamVid/")

        return object_path

    @staticmethod
    def auto(object_path):
        object_name = path.name(object_path).lower()

        if "airs" in object_name:
            return DatasetSource.AIRS

        if "camvid" in object_name:
            return DatasetSource.CAMVID

        raise NameError(f"unknown dataset source: {object_name}")
