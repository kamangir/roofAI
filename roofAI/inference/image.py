import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from blue_objects.env import ABCLI_AWS_REGION

from roofAI import NAME
from roofAI.logger import logger


NAME = module.name(__file__, NAME)


# https://github.com/aws/deep-learning-containers/blob/master/available_images.md
repository_name = "pytorch-inference"
# image_tag = "2.1.0-gpu-py310-cu118-ubuntu20.04-ec2"
image_tag = "2.1.0-cpu-py310-ubuntu20.04-ec2"
image_name = "763104351884.dkr.ecr.{}.amazonaws.com/{}:{}".format(
    ABCLI_AWS_REGION,
    repository_name,
    image_tag,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(NAME)

    parser.add_argument(
        "task",
        type=str,
        help="get",
    )
    parser.add_argument(
        "--what",
        type=str,
        help="name|repo|tag",
    )
    args = parser.parse_args()

    success = False
    if args.task == "get":
        success = True
        print(
            image_name
            if args.what == "name"
            else (
                repository_name
                if args.what == "repo"
                else image_tag if args.what == "tag" else f"unknown-{args.what}"
            )
        )
    else:
        success = None

    sys_exit(logger, NAME, args.task, success)
