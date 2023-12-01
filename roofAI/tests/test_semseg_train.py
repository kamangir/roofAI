import pytest
from abcli.modules import objects
from abcli.plugins import cache
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

    assert isinstance(
        train(
            dataset_path=objects.object_path(
                cache.read(f"roofAI_ingest_{dataset_source}_v1")
            ),
            model_path=objects.object_path(objects.unique_object()),
            classes=classes,
            do_register=True,
            suffix="pytest",
        ),
        SemSegModel,
    )

    predict(
        model_path=objects.object_path(
            cache.read(f"roofAI_semseg_model_{dataset_source}_pytest")
        ),
        dataset_path=objects.object_path(
            cache.read(f"roofAI_ingest_{dataset_source}_v1")
        ),
        prediction_path=objects.object_path(objects.unique_object()),
        device="cpu",
    )
