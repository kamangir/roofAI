from abcli.modules import objects
from roofAI.ingest.dataset import RoofAIDataset, Kind
from abcli.plugins import cache
import numpy as np


def test_RoofAIDataset():
    dataset = RoofAIDataset(objects.object_path(cache.read("roofAI_ingest_CamVid_v1")))

    subset = "test"
    index = 4

    record_id = dataset.subsets[subset][index]
    assert record_id

    image = dataset.get_matrix(subset, record_id, Kind.IMAGE, log=True)
    assert image.shape == (360, 480, 3)
    assert image.dtype == np.uint8

    mask = dataset.get_matrix(subset, record_id, Kind.MASK, log=True)
    assert mask.shape == (360, 480)
    assert mask.dtype == np.uint8
