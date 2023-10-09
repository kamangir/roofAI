import argparse
from roofAI import NAME, VERSION, DESCRIPTION
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    NAME,
    description=f"{NAME}-{VERSION}: {DESCRIPTION}",
)
parser.add_argument(
    "task",
    type=str,
    help="",
)
args = parser.parse_args()

success = False
if args.task == "void":
    success = True
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
