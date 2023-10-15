import argparse
from roofAI import NAME, VERSION
from roofAI.semseg.interface import predict, train
from roofAI.semseg import Profile
from abcli.logging import crash_report
from abcli import logging
import logging

logger = logging.getLogger(__name__)

NAME = f"{NAME}.semseg"

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "task",
    type=str,
    help="predict|train",
)
parser.add_argument(
    "--activation",
    type=str,
    default="sigmoid",
    help="sigmoid or None for logits or softmax2d for multi-class segmentation",
)
parser.add_argument(
    "--classes",
    type=str,
    default="car",
    help="one+two+three+four",
)
parser.add_argument(
    "--dataset_path",
    type=str,
)
parser.add_argument(
    "--device",
    type=str,
    default="cpu",
    help="cpu|cuda",
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
    "--model_path",
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
        success = predict(
            args.model_path,
            args.dataset_path,
            args.prediction_path,
            args.device,
            profile,
        )
    elif args.task == "train":
        success = train(
            args.dataset_path,
            args.model_path,
            profile,
            encoder_name=args.encoder_name,
            encoder_weights=args.encoder_weights,
            classes=args.classes.split("+"),
            activation=args.activation,
            device=args.device,
        )
    else:
        logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
