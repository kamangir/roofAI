import pytest
from abcli import string
from roofAI.inference.classes import InferenceClient, InferenceObject


@pytest.mark.parametrize(
    "model_name",
    [
        ("model-2023-12-02-19-58-34-09697"),
    ],
)
def test_inference_client(model_name):
    inference_client = InferenceClient(verbose=True)

    assert inference_client.create(
        InferenceObject.MODEL,
        model_name,
    )

    assert inference_client.create(
        InferenceObject.ENDPOINT_CONFIG,
        model_name,
    )

    assert inference_client.create(
        InferenceObject.ENDPOINT,
        "{}-{}".format(model_name, string.random_(8)),
        model_name,
    )
