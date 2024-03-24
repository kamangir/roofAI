from abcli.modules import objects
from abcli.plugins.testing import download_object
from roofAI.semseg.interface import predict
from abcli.plugins import cache


def test_semseg_predict():
    model_object_name = cache.read("roofAI_semseg_model_CamVid_v1")
    assert download_object(model_object_name)

    dataset_object_name = cache.read("roofAI_ingest_CamVid_v1")
    assert download_object(dataset_object_name)

    predict(
        model_path=objects.object_path(model_object_name),
        dataset_path=objects.object_path(dataset_object_name),
        prediction_path=objects.object_path(
            objects.unique_object("test_semseg_predict")
        ),
        device="cpu",
    )
