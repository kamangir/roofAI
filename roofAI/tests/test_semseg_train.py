from abcli.modules import objects
from abcli.plugins import cache
from roofAI.semseg.interface import train


def test_semseg_train():
    success, _ = train(
        dataset_path=objects.object_path(cache.read("roofAI_ingest_CamVid_v1")),
        model_path=objects.object_path(objects.unique_object("test_semseg_train")),
    )
    assert success

    # TODO: test the model
