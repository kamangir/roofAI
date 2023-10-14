import argparse
import os
from abcli import path
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
    help="ingest|predict|train",
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
    default=-1,
    help="0|1|-1",
)
parser.add_argument(
    "--encoder_name",
    type=str,
    default="se_resnext50_32x4d",
)
parser.add_argument(
    "--encoder_weights",
    type=str,
    default="imagenet",
)
parser.add_argument(
    "--classes",
    type=str,
    default="car",
    help="one+two+three+four",
)
parser.add_argument(
    "--activation",
    type=str,
    default="sigmoid",
    help="sigmoid or None for logits or softmax2d for multi-class segmentation",
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
dataset_is_camvid = args.dataset_is_camvid
if dataset_is_camvid == -1:
    dataset_is_camvid = "camvid" in path.name(dataset_path).lower()
if dataset_is_camvid:
    dataset_path = os.path.join(dataset_path, "SegNet-Tutorial/CamVid/")
logger.info(f"dataset_path: {dataset_path}")

if success:
    success = False
    if args.task == "ingest":
        ...
    elif args.task == "predict":
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
            encoder_name=args.encoder_name,
            encoder_weights=args.encoder_weights,
            classes=args.classes.split("+"),
            activation=args.activation,
            device=args.device,
        )

        success = True
    else:
        logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
