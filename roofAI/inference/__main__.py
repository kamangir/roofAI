import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from blue_options.logger import crash_report

from roofAI import NAME
from roofAI.inference.classes import InferenceClient, InferenceObject
from roofAI.inference.image import image_name
from roofAI.inference.endpoints import invoke_endpoint
from roofAI.semseg import Profile
from roofAI.logger import logger

NAME = module.name(__file__, NAME)

list_of_tasks = "create|delete|describe|invoke|list"
parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=list_of_tasks,
)
parser.add_argument(
    "--config_suffix",
    type=str,
)
parser.add_argument(
    "--dataset_path",
    type=str,
)
parser.add_argument(
    "--endpoint_name",
    type=str,
)
parser.add_argument(
    "--suffix",
    type=str,
)
parser.add_argument(
    "--object_type",
    type=str,
    default="model",
    help="model,endpoint_config,endpoint",
)
parser.add_argument(
    "--object_name",
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
    "--verbose",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--verify",
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

inference_client = None
if args.task != "invoke":
    inference_client = InferenceClient(
        image_name=image_name,
        verbose=bool(args.verbose),
    )
object_type = InferenceObject[args.object_type.upper()]

success = args.task in list_of_tasks.split("|")
if args.task == "create":
    if object_type == InferenceObject.MODEL:
        success = inference_client.create_model(
            name=args.object_name,
            verify=bool(args.verify),
        )
    elif object_type == InferenceObject.ENDPOINT_CONFIG:
        success = inference_client.create_endpoint_config(
            name=f"config-{args.object_name}-{args.suffix}",
            model_name=args.object_name,
            verify=bool(args.verify),
        )
    elif object_type == InferenceObject.ENDPOINT:
        success = inference_client.create_endpoint(
            name=f"endpoint-{args.object_name}-{args.suffix}",
            config_name=f"config-{args.object_name}-{args.config_suffix}",
            verify=bool(args.verify),
        )
    else:
        success = False
elif args.task == "delete":
    success = inference_client.delete(
        what=object_type,
        name=args.object_name,
    )
elif args.task == "describe":
    success, response = inference_client.describe(
        what=object_type,
        name=args.object_name,
    )
    if success:
        logger.info(response)
elif args.task == "invoke":
    success = invoke_endpoint(
        endpoint_name=args.endpoint_name,
        dataset_path=args.dataset_path,
        prediction_path=args.prediction_path,
        profile=profile,
        verbose=bool(args.verbose),
    )
elif args.task == "list":
    success = True
    output = inference_client.list_(
        what=object_type,
        name=args.object_name,
    )

    logger.info(f"{len(output):,} {args.object_type}(s)")
    for index, item in enumerate(output):
        logger.info(f"#{index}: {item}")
else:
    success = None

sys_exit(logger, NAME, args.task, success)
