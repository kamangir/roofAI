import pytest
from abcli.modules import objects
from abcli.plugins import cache
from abcli.plugins.testing import download_object
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
    cache.write(f"roofAI_semseg_model_{dataset_source}_pytest", "void")

    dataset_object_name = cache.read(f"roofAI_ingest_{dataset_source}_v1")
    assert download_object(dataset_object_name)

    assert isinstance(
        train(
            dataset_path=objects.object_path(dataset_object_name),
            model_path=objects.object_path(objects.unique_object()),
            classes=classes,
            do_register=True,
            suffix="pytest",
        ),
        SemSegModel,
    )

    model_object_name = cache.read(f"roofAI_semseg_model_{dataset_source}_pytest")

    predict(
        model_path=objects.object_path(model_object_name),
        dataset_path=objects.object_path(dataset_object_name),
        prediction_path=objects.object_path(objects.unique_object()),
        device="cpu",
    )
