import argparse
import os
from roofAI import NAME, VERSION
from roofAI.semseg.model import SemSegModel
from roofAI.semseg import Profile
from abcli.logging import crash_report
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}.semseg",
    description=f"{NAME}-{VERSION}.semseg",
)
parser.add_argument(
    "task",
    type=str,
    help="predict",
)
parser.add_argument(
    "--model_path",
    type=str,
)
parser.add_argument(
    "--dataset_path",
    type=str,
)
parser.add_argument(
    "--prediction_path",
    type=str,
)
parser.add_argument(
    "--profile",
    type=str,
    default="VALIDATION",
    help="FULL|QUICK|VALIDATION",
)
args = parser.parse_args()

success = True
try:
    profile = Profile[args.profile]
    logger.info(f"profile: {profile}")
except:
    crash_report(f"bad profile: {args.profile}")
    success = False

if success:
    success = False
    if args.task == "predict":
        model = SemSegModel(
            model_filename=os.path.join(args.model_path, "model.pth"),
            profile=args.profile,
        )

        model.predict(
            dataset_path=os.path.join(args.dataset_path, "SegNet-Tutorial/CamVid/"),
            output_path=args.prediction_path,
            in_notebook=False,
        )

        success = True
    else:
        logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
