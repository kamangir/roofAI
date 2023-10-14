import argparse
import os
from roofAI import NAME, VERSION
from roofAI.semseg.model import SemSegModel
from roofAI.semseg.train import SemSegModelTrainer
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
parser.add_argument(
    "--device",
    type=str,
    default="cpu",
    help="cpu|cuda",
)
parser.add_argument(
    "--dataset_is_camvid",
    type=int,
    default=1,
    help="0|1",
)
args = parser.parse_args()

success = True
try:
    profile = Profile[args.profile]
    logger.info(f"profile: {profile}")
except:
    crash_report(f"bad profile: {args.profile}")
    success = False

dataset_path = args.dataset_path
if args.dataset_is_camvid:
    dataset_path = os.path.join(dataset_path, "SegNet-Tutorial/CamVid/")
logger.info(f"dataset_path: {dataset_path}")

if success:
    success = False
    if args.task == "predict":
        model = SemSegModel(
            model_filename=os.path.join(args.model_path, "model.pth"),
            profile=profile,
        )

        model.predict(
            dataset_path=dataset_path,
            output_path=args.prediction_path,
            device=args.device,
            in_notebook=False,
        )

        success = True
    elif args.task == "train":
        trainer = SemSegModelTrainer(
            dataset_path=dataset_path,
            model_path=args.model_path,
            in_notebook=False,
            profile=profile,
        )

        model = trainer.train(
            device=args.device,
        )
    else:
        logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
