import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from blue_options.logger import crash_report
from blue_objects import path

from roofai import NAME
from roofai.semseg.interface import predict, train
from roofai.semseg import Profile
from roofai.logger import logger

NAME = module.name(__file__, NAME)


list_of_tasks = "predict|train"

parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=list_of_tasks,
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
    default="",
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
parser.add_argument(
    "--epoch_count",
    type=int,
    default=-1,
    help="-1: according to profile",
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
    success = args.task in list_of_tasks.split("|")
    if args.task == "predict":
        if not path.create(args.prediction_path):
            success = False
        else:
            predict(
                model_path=args.model_path,
                dataset_path=args.dataset_path,
                prediction_path=args.prediction_path,
                device=args.device,
                profile=profile,
            )
    elif args.task == "train":
        train(
            dataset_path=args.dataset_path,
            model_path=args.model_path,
            encoder_name=args.encoder_name,
            encoder_weights=args.encoder_weights,
            classes=args.classes.split("+"),
            activation=args.activation,
            device=args.device,
            profile=profile,
            epoch_count=args.epoch_count,
        )
    else:
        success = None

sys_exit(logger, NAME, args.task, success)
