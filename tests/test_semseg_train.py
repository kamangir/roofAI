from abcli.modules import objects
from roofAI.semseg.interface import train


def test_semseg_train():
    success, _ = train(
        dataset_path=objects.object_path("roofAI-CamVid-v2"),
        model_path=objects.object_path(objects.unique_object("test_semseg_train")),
    )
    assert success

    # TODO: test the model
