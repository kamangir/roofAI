import numpy as np
import torch
from six import BytesIO


# https://github.com/aws/sagemaker-python-sdk/blob/master/doc/frameworks/pytorch/using_pytorch.rst#serve-a-pytorch-model
def input_fn(request_body, request_content_type):
    """An input_fn that loads a pickled tensor"""
    if request_content_type == "application/python-pickle":
        return torch.load(BytesIO(request_body))

    # Handle other content-types here or raise an Exception
    # if the content type is not supported.
    raise NameError(f"{request_content_type} content type not supported.")


def predict_fn(input_data, model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    with torch.no_grad():
        return model(input_data.to(device))


def output_fn(prediction, content_type, context):
    print(f"prediction={prediction}, content_type={content_type}, context={context}")
    # return a byte array of data serialized to content_type.
