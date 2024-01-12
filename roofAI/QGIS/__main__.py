import argparse
from roofAI.QGIS import NAME
from roofAI import VERSION
from roofAI.QGIS.seed import generate_seed
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "task",
    type=str,
    help="generate_seed",
)
args = parser.parse_args()

success = False
if args.task == "generate_seed":
    success = seed = generate_seed()
    if success:
        print(seed)
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
