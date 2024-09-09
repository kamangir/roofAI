import pytest

from blue_objects import objects
from abcli.plugins import cache

from roofAI.dataset.ingest.AIRS import ingest_AIRS


@pytest.mark.skip("roofAI_ingest_AIRS_cache is a large object cached by `roof ingest`.")
def test_ingest_AIRS():
    assert ingest_AIRS(
        cache_path=objects.object_path(cache.read("roofAI_ingest_AIRS_cache")),
        ingest_path=objects.object_path(objects.unique_object("test_ingest_AIRS")),
        counts={
            "test": 2,
            "train": 2,
            "val": 2,
        },
        log=True,
    )
