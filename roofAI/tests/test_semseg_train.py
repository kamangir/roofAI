import pytest

from blue_options.string import random
from blue_objects import objects
from blue_objects.mlflow import cache

from roofAI.semseg.interface import predict, train
from roofAI.semseg.model import SemSegModel


@pytest.mark.parametrize(
    "dataset_source, classes",
    [
        (
            "AIRS",
            ["roof"],
        ),
        (
            "CamVid",
            ["car"],
        ),
    ],
)
def test_semseg_train(dataset_source, classes):
    success, dataset_object_name = cache.read(f"roofAI_ingest_{dataset_source}_v1")
    assert success
    assert dataset_object_name

    assert objects.download(dataset_object_name)

    model_object_name = objects.unique_object("test_semseg_train-model")

    model = train(
        dataset_path=objects.object_path(dataset_object_name),
        model_path=objects.object_path(model_object_name),
        classes=classes,
    )
    assert isinstance(model, SemSegModel)

    predict(
        model_path=objects.object_path(model_object_name),
        dataset_path=objects.object_path(dataset_object_name),
        prediction_path=objects.object_path(objects.unique_object()),
        device="cpu",
    )
