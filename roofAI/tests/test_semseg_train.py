from abcli.modules import objects
from abcli.plugins import cache
from roofAI.semseg.interface import predict, train
from roofAI.semseg.model import SemSegModel


def test_semseg_train():
    cache.write("roofAI_semseg_model_CamVid_void_py", "void")

    assert isinstance(
        train(
            dataset_path=objects.object_path(cache.read("roofAI_ingest_CamVid_v1")),
            model_path=objects.object_path(objects.unique_object("test_semseg_train")),
            register=True,
            suffix="void_py",
        ),
        SemSegModel,
    )

    predict(
        model_path=objects.object_path(
            cache.read("roofAI_semseg_model_CamVid_void_py")
        ),
        dataset_path=objects.object_path(cache.read("roofAI_ingest_CamVid_v1")),
        prediction_path=objects.object_path(
            objects.unique_object("test_semseg_predict")
        ),
        device="cpu",
    )
