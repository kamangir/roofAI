from blue_objects import objects
from blue_objects.mlflow import cache

from roofAI.semseg.interface import predict


def test_semseg_predict():
    success, model_object_name = cache.read("roofAI_semseg_model_CamVid_v1")
    assert success and model_object_name

    assert objects.download(model_object_name)

    success, dataset_object_name = cache.read("roofAI_ingest_CamVid_v1")
    assert success and dataset_object_name

    assert objects.download(dataset_object_name)

    prediction_object_name = objects.unique_object("test_semseg_predict")

    predict(
        model_path=objects.object_path(model_object_name),
        dataset_path=objects.object_path(dataset_object_name),
        prediction_path=objects.object_path(prediction_object_name),
        device="cpu",
    )
