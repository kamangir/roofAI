import pytest

from blue_objects import objects
from blue_objects.mlflow import cache

from roofAI.dataset.ingest.AIRS import ingest_AIRS


@pytest.mark.skip("roofAI_ingest_AIRS_cache is a large object cached by `roof ingest`.")
def test_ingest_AIRS():
    success, cache_object_name = cache.read("roofAI_ingest_AIRS_cache")
    assert success and cache_object_name

    dataset_object_name = objects.unique_object("test_ingest_AIRS")

    assert ingest_AIRS(
        cache_path=objects.object_path(cache_object_name),
        ingest_path=objects.object_path(dataset_object_name),
        counts={
            "test": 2,
            "train": 2,
            "val": 2,
        },
        log=True,
    )
