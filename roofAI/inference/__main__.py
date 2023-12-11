import argparse
from roofAI import NAME, VERSION
from roofAI.inference.classes import InferenceClient, InferenceObject
from abcli import logging
import logging

logger = logging.getLogger(__name__)

NAME = f"{NAME}.inference"

list_of_tasks = "create|delete|list"

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "task",
    type=str,
    help=list_of_tasks,
)
parser.add_argument(
    "--config_name",
    type=str,
    help="required when creating an endpoint.",
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
    "--verbose",
    type=int,
    default=0,
    help="0|1",
)
args = parser.parse_args()

inference_client = InferenceClient(verbose=bool(args.verbose))

object_type = InferenceObject[args.object_type.upper()]

success = args.task in list_of_tasks.split("|")
if args.task == "create":
    success = inference_client.create(
        what=object_type,
        name=args.object_name,
        config_name=args.config_name,
    )
elif args.task == "delete":
    sucess = inference_client.delete(
        what=object_type,
        name=args.object_name,
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
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
