import os
import boto3
from tqdm import tqdm

from blue_objects import path, file

from roofAI.semseg import Profile
from roofAI.dataset.classes import RoofAIDataset
from roofAI.logger import logger


def invoke_endpoint(
    endpoint_name: str,
    dataset_path: str,
    prediction_path: str,
    profile: Profile = Profile.VALIDATION,
    verbose: bool = False,
) -> bool:
    logger.info(
        "invoke_endpoint({}:{}) -{}-> {}".format(
            endpoint_name,
            dataset_path,
            profile,
            prediction_path,
        )
    )

    # https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints-invoke.html
    runtime = boto3.client("sagemaker-runtime")
    logger.info(f"runtime: {runtime}")

    if not path.create(prediction_path):
        return False

    dataset = RoofAIDataset(dataset_path)
    image_dir = os.path.join(dataset.dataset_path, "test")
    ids = os.listdir(image_dir)
    if profile.data_count != -1:
        ids = ids[: profile.data_count]

    metadata = {}
    for image_id in tqdm(ids):
        metadata[image_id] = {}
        image_filename = os.path.join(image_dir, image_id)

        content_type = "<request-mime-type>"
        payload = image_filename

        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Body=payload,
        )
        if verbose:
            logger.info(response)

        file.save_json(
            os.path.join(
                prediction_path,
                f"{file.name(image_id)}.json",
            ),
            response,
            log=True,
        )

    return file.save_json(
        os.path.join(prediction_path, "metadata.json"),
        metadata,
        log=True,
    )
