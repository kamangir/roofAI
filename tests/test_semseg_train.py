from abcli.modules import objects
from roofAI.semseg.interface import train_model
from roofAI.semseg import Profile


def test_semseg_train_model():
    success, model = train_model(
        dataset_path=objects.object_path("roofAI-CamVid-v2"),
        model_path=objects.object_path(
            objects.unique_object("test_semseg_train_model")
        ),
        profile=Profile.VALIDATION,
    )
    assert success

    # TODO: test the model
