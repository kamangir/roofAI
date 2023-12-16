from abcli import path
from roofAI.semseg import Profile
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

    return True
