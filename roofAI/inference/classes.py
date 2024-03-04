import boto3
from enum import Enum, auto
from typing import List, Any, Tuple
from sagemaker import image_uris
import sagemaker
from roofAI.logger import logger


class InferenceObject(Enum):
    MODEL = auto()
    ENDPOINT_CONFIG = auto()
    ENDPOINT = auto()


class InferenceClient:
    def __init__(
        self,
        image_name: str = "",
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

        self.image_name = (
            image_uris.retrieve("xgboost", self.region, "0.90-1")
            if not image_name
            else image_name
        )

        logger.info(f"{self.__class__.__name__} created: {self.image_name}")

    def create_model(
        self,
        name: str,
        verify: bool = True,
    ) -> bool:
        object_type = InferenceObject.MODEL
        logger.info(f"create_model({name})...")

        if self.list_(object_type, name):
            if not self.delete(object_type, name):
                return False

        # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-model
        response = self.client.create_model(
            ModelName=name,
            ExecutionRoleArn=self.sagemaker_role,
            Containers=[
                {
                    "Image": self.image_name,
                    "Mode": "SingleModel",
                    "ModelDataUrl": f"s3://kamangir/bolt/{name}.tar.gz",
                }
            ],
        )
        if self.verbose:
            logger.info(response)

        return bool(self.list_(object_type, name)) if verify else True

    def create_endpoint_config(
        self,
        name: str,
        model_name: str,
        verify: bool = True,
    ) -> bool:
        object_type = InferenceObject.ENDPOINT_CONFIG
        logger.info(f"create_endpoint_config({name}:{model_name})...")

        if self.list_(object_type, name):
            if not self.delete(object_type, name):
                return False

        # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-config
        response = self.client.create_endpoint_config(
            EndpointConfigName=name,
            ProductionVariants=[
                {
                    "ModelName": model_name,
                    "VariantName": "AllTraffic",
                    "ServerlessConfig": {
                        "MemorySizeInMB": 2048,
                        "MaxConcurrency": 20,
                        # "ProvisionedConcurrency": 10,
                    },
                }
            ],
        )
        if self.verbose:
            logger.info(response)

        return bool(self.list_(object_type, name)) if verify else True

    def create_endpoint(
        self,
        name: str,
        config_name: str = "",
        verify: bool = True,
    ) -> bool:
        object_type = InferenceObject.ENDPOINT
        logger.info(f"create_endpoint({name}:{config_name})...")

        if self.list_(object_type, name):
            if not self.delete(object_type, name):
                return False

        # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-endpoint
        response = self.client.create_endpoint(
            EndpointName=name,
            EndpointConfigName=config_name,
        )
        if self.verbose:
            logger.info(response)

        return bool(self.list_(object_type, name)) if verify else True

    def delete(
        self,
        what: InferenceObject,
        name: str,
    ) -> bool:
        response = {}
        if not isinstance(what, InferenceObject):
            logger.error(f"delete({name}): unknown object: {what}.")
            return False

        logger.info(f"delete({what},{name})")

        if what == InferenceObject.MODEL:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model.html
            response = self.client.delete_model(ModelName=name)

        if what == InferenceObject.ENDPOINT_CONFIG:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_endpoint_config.html
            response = self.client.delete_endpoint_config(EndpointConfigName=name)

        if what == InferenceObject.ENDPOINT:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_endpoint.html
            try:
                response = self.client.delete_endpoint(EndpointName=name)
            except Exception as e:
                logger.error(e)
                return False

        if self.verbose:
            logger.info(f"delete({what},{name}): {response}")

        return True

    def describe(
        self,
        what: InferenceObject,
        name: str,
    ) -> Tuple[bool, Any]:
        response = {}
        if not isinstance(what, InferenceObject):
            logger.error(f"describe({name}): unknown object: {what}.")
            return False, response
        if what != InferenceObject.ENDPOINT:
            logger.error(f"describe({name}): cannot describe {what}.")
            return False, response

        logger.info(f"describe({what},{name})")

        if what == InferenceObject.ENDPOINT:
            # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-describe.html
            response = self.client.describe_endpoint(EndpointName=name)

        if self.verbose:
            logger.info(f"describe({what},{name}): {response}")

        return True, response

    def list_(
        self,
        what: InferenceObject,
        name: str,
    ) -> List[Any]:
        output = False
        response = {}
        if not isinstance(what, InferenceObject):
            logger.error(f"delete({name}): unknown object: {what}.")
            return False

        if what == InferenceObject.MODEL:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_models.html
            response = self.client.list_models(NameContains=name)
            output = response["Models"]

        if what == InferenceObject.ENDPOINT_CONFIG:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoint_configs.html
            response = self.client.list_endpoint_configs(NameContains=name)
            output = response["EndpointConfigs"]

        if what == InferenceObject.ENDPOINT:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoints.html
            response = self.client.list_endpoints(NameContains=name)
            output = response["Endpoints"]

        if self.verbose:
            logger.info(f"list({what},{name}): {response}")

        return output
