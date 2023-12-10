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
    ENDPOINT = auto()


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

    def create(
        self,
        what: InferenceObject,
        name: str,
        config_name: str = "",
        verify: bool = True,
    ) -> bool:
        if not isinstance(what, InferenceObject):
            logger.error(f"create({name}): unknown object: {what}.")
            return False

        config_name = name if not config_name else config_name
        logger.info(
            "create({},{}{})...".format(
                what,
                "{}->".format(config_name) if what == InferenceObject.ENDPOINT else "",
                name,
            )
        )

        if self.exists(what, name):
            logger.info(f"{what} {name} already exists, will delete first.")
            if not self.delete(what, name):
                return False

        response = {}
        if what == InferenceObject.MODEL:
            # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-model
            response = self.client.create_model(
                ModelName=name,
                ExecutionRoleArn=self.sagemaker_role,
                Containers=[
                    {
                        "Image": self.container,
                        "Mode": "SingleModel",
                        "ModelDataUrl": f"s3://kamangir/bolt/{name}.tar.gz",
                    }
                ],
            )

        if what == InferenceObject.ENDPOINT_CONFIG:
            # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-config
            response = self.client.create_endpoint_config(
                EndpointConfigName=name,
                ProductionVariants=[
                    {
                        "ModelName": name,
                        "VariantName": "AllTraffic",
                        "ServerlessConfig": {
                            "MemorySizeInMB": 2048,
                            "MaxConcurrency": 20,
                            # "ProvisionedConcurrency": 10,
                        },
                    }
                ],
            )

        if what == InferenceObject.ENDPOINT:
            # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-create.html#serverless-endpoints-create-endpoint
            response = self.client.create_endpoint(
                EndpointName=name,
                EndpointConfigName=config_name,
            )

        if self.verbose:
            logger.info(f"create({what},{name}): {response}")

        return self.exists(what, name) if verify else True

    def delete(
        self,
        what: InferenceObject,
        name: str,
    ) -> bool:
        response = {}
        if not isinstance(what, InferenceObject):
            logger.error(f"delete({name}): unknown object: {what}.")
            return False

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

    def exists(
        self,
        what: InferenceObject,
        name: str,
    ) -> bool:
        output = False
        response = {}
        if not isinstance(what, InferenceObject):
            logger.error(f"delete({name}): unknown object: {what}.")
            return False

        if what == InferenceObject.MODEL:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_models.html
            response = self.client.list_models(NameContains=name)
            output = bool(response["Models"])

        if what == InferenceObject.ENDPOINT_CONFIG:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoint_configs.html
            response = self.client.list_endpoint_configs(NameContains=name)
            output = bool(response["EndpointConfigs"])

        if what == InferenceObject.ENDPOINT:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoints.html
            response = self.client.list_endpoints(NameContains=name)
            output = bool(response["Endpoints"])

        if self.verbose:
            logger.info(f"exists({what},{name}): {response}")

        return output
