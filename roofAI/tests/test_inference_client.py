import pytest
from abcli import string
from roofAI.inference.classes import InferenceClient


@pytest.mark.parametrize(
    "model_name",
    [
        ("model-2023-12-02-19-58-34-09697"),
    ],
)
def test_inference_client(model_name):
    inference_client = InferenceClient(verbose=True)

    assert inference_client.create_model(
        name=model_name,
    )

    config_name = "config-{}-{}".format(model_name, string.random_(8))
    assert inference_client.create_endpoint_config(
        name=config_name,
        model_name=model_name,
    )

    endpoint_name = "endpoint-{}-{}".format(model_name, string.random_(8))
    assert inference_client.create_endpoint(
        name=endpoint_name,
        config_name=config_name,
    )
