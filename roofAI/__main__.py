import argparse
from roofAI import NAME, VERSION, DESCRIPTION
from roofAI.logger import logger
from blueness.argparse.generic import sys_exit

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "task",
    type=str,
    help="version",
)
parser.add_argument(
    "--show_description",
    type=bool,
    default=0,
    help="0|1",
)
args = parser.parse_args()

success = False
if args.task == "version":
    print(
        "{}-{}{}".format(
            NAME,
            VERSION,
            "\\n{}".format(DESCRIPTION) if args.show_description else "",
        )
    )
    success = True
else:
    success = None

sys_exit(logger, NAME, args.task, success)
