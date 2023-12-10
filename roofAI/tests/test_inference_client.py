import pytest
from roofAI.inference.classes import InferenceClient, InferenceObject


@pytest.mark.parametrize(
    "model_name",
    [
        ("model-2023-12-03-11-24-39-75649"),
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
