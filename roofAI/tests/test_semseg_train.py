import pytest

from blue_objects import objects

from roofAI import env
from roofAI.semseg.interface import predict, train
from roofAI.semseg.model import SemSegModel


@pytest.mark.parametrize(
    "dataset_source, classes",
    [
        (
            env.TEST_roofAI_ingest_AIRS_v1,
            ["roof"],
        ),
        (
            env.TEST_roofAI_ingest_CamVid_v1,
            ["car"],
        ),
    ],
)
def test_semseg_train(dataset_object_name, classes):
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
