import boto3
from enum import Enum, auto
from sagemaker import image_uris
import sagemaker
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class InferenceObject(Enum):
    MODEL = auto()
    ENDPOINT_CONFIG = auto()


class InferenceClient(object):
    def __init__(
        self,
        verbose: bool = False,
    ):
        self.verbose = verbose

        self.region = boto3.Session().region_name
        self.client = boto3.client("sagemaker", region_name=self.region)

        # Role to give SageMaker permission to access AWS services.
        # https://github.com/aws-solutions-library-samples/guidance-for-training-an-aws-deepracer-model-using-amazon-sagemaker/issues/47#issuecomment-607238430
        try:
            self.sagemaker_role = sagemaker.get_execution_role()
        except ValueError:
            logger.info("sagemaker_role: defaulting to local.")
            iam = boto3.client("iam")
            self.sagemaker_role = iam.get_role(RoleName="Sagemaker-Access")["Role"][
                "Arn"
            ]

        # Get container image (prebuilt example)
        self.container = image_uris.retrieve("xgboost", self.region, "0.90-1")

        logger.info(f"{self.__class__.__name__} created.")

    def create_model(
        self,
        model_name: str,
        verify: bool = True,
    ) -> bool:
        logger.info(f"create_model({model_name})...")

        if self.exists(InferenceObject.MODEL, model_name):
            logger.info(f"{model_name} already exists, will delete first.")
            self.delete_model(model_name)

        # Create the model
        response = self.client.create_model(
            ModelName=model_name,
            ExecutionRoleArn=self.sagemaker_role,
            Containers=[
                {
                    "Image": self.container,
                    "Mode": "SingleModel",
                    "ModelDataUrl": f"s3://kamangir/bolt/{model_name}.tar.gz",
                }
            ],
        )
        if self.verbose:
            logger.info(f"create_model({model_name}): {response}")

        return self.exists(InferenceObject.MODEL, model_name) if verify else True

    def delete_model(self, model_name: str):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model.html#
        response = self.client.delete_model(ModelName=model_name)
        if self.verbose:
            logger.info(f"delete_model({model_name}): {response}")

    def exists(
        self,
        what: InferenceObject,
        name: str,
    ) -> bool:
        if what == InferenceObject.MODEL:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_models.html
            response = self.client.list_models(NameContains=name)

            if self.verbose:
                logger.info(f"exists({what},{name}): {response}")

            return bool(response["Models"])

        if what == InferenceObject.ENDPOINT_CONFIG:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoint_configs.html
            response = self.client.list_endpoint_configs(NameContains=name)

            if self.verbose:
                logger.info(f"exists({what},{name}): {response}")

            return bool(response["EndpointConfigs"])

        logger.error(f"exists({name}): unknown object: {what}.")
        return False
