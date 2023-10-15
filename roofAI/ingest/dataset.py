import os
from enum import Enum, auto as auto_
from abcli import path
from abcli import file
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class RoofAIDataset(object):
    def __init__(self, dataset_path):
        self.path = dataset_path
        success, self.metadata = file.load_yaml(
            os.path.join(self.path, "metadata.yaml")
        )
        assert success

    @property
    def dataset_path(self):
        return (
            os.path.join(self.path, "SegNet-Tutorial/CamVid/")
            if self.source == "CamVid"
            else self.path
        )

    @property
    def source(self):
        return self.metadata.get("source", "unknown")
