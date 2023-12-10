import boto3
import json
import sagemaker
from sagemaker import image_uris
from typing import Tuple, Any
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def create_model_and_endpoint(
    model_name: str,
    verbose: bool = False,
) -> bool:
    logger.info("create_model_and_endpoint({})".format(model_name))

    model_url = f"s3://kamangir/bolt/{model_name}.tar.gz"

    region = boto3.Session().region_name
    client = boto3.client("sagemaker", region_name=region)

    # Role to give SageMaker permission to access AWS services.
    # https://github.com/aws-solutions-library-samples/guidance-for-training-an-aws-deepracer-model-using-amazon-sagemaker/issues/47#issuecomment-607238430
    try:
        sagemaker_role = sagemaker.get_execution_role()
    except ValueError:
        logger.info("sagemaker_role: defaulting to local.")
        iam = boto3.client("iam")
        sagemaker_role = iam.get_role(RoleName="Sagemaker-Access")["Role"]["Arn"]

    # Get container image (prebuilt example)
    container = image_uris.retrieve("xgboost", region, "0.90-1")

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_models.html
    response = client.list_models(NameContains=model_name)
    if verbose:
        logger.info("list_models: {}".format(response))
    model_found = bool(response["Models"])

    if model_found:
        logger.info("model already exists, will delete first.")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model.html#
        response = client.delete_model(ModelName=model_name)
        if verbose:
            logger.info("delete_model: {}".format(response))

    # Create the model
    response = client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=sagemaker_role,
        Containers=[
            {
                "Image": container,
                "Mode": "SingleModel",
                "ModelDataUrl": model_url,
            }
        ],
    )
    if verbose:
        logger.info("create_model: {}".format(response))

    response = client.list_models(NameContains=model_name)
    if not response["Models"]:
        logger.error("model was not created: {}.".format(response))
        return False
    if verbose:
        logger.info("Models: {}".format(response["Models"]))

    return True
