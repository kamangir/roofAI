import os
from abcli import path
from tqdm import tqdm
from roofAI.semseg import Profile
from roofAI.dataset import RoofAIDataset
from abcli import logging
import logging

logger = logging.getLogger(__name__)


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

    if not path.create(prediction_path):
        return False

    dataset = RoofAIDataset(dataset_path)
    image_dir = os.path.join(dataset.dataset_path, "test")
    ids = os.listdir(image_dir)
    if profile.data_count != -1:
        ids = ids[: profile.data_count]

    for image_id in tqdm(ids):
        image_filename = os.path.join(image_dir, image_id)
        logger.info(f"🪄 {image_filename}...")

    return True
