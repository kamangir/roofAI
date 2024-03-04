import argparse
from roofAI import NAME, VERSION, DESCRIPTION
from roofAI.logger import logger

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
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
