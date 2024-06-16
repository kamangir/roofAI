import argparse
from abcli import env
from roofAI import VERSION
from roofAI.inference import NAME
from roofAI.logger import logger
from blueness.argparse.generic import sys_exit

NAME = f"{NAME}.image"


# https://github.com/aws/deep-learning-containers/blob/master/available_images.md
repository_name = "pytorch-inference"
# image_tag = "2.1.0-gpu-py310-cu118-ubuntu20.04-ec2"
image_tag = "2.1.0-cpu-py310-ubuntu20.04-ec2"
image_name = "763104351884.dkr.ecr.{}.amazonaws.com/{}:{}".format(
    env.abcli_aws_region,
    repository_name,
    image_tag,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        f"python3 -m {NAME}",
        description=f"{NAME}-{VERSION}",
    )
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
