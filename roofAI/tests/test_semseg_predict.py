from abcli.modules import objects
from roofAI.semseg.interface import predict
from abcli.plugins import cache


def test_semseg_predict():
    assert predict(
        model_path=objects.object_path(cache.read("latest_CamVid_model")),
        dataset_path=objects.object_path("roofAI-CamVid-v2"),
        prediction_path=objects.object_path(
            objects.unique_object("test_semseg_predict")
        ),
        device="cpu",
    )
