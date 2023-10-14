import argparse
from roofAI.ingest.AIRS import ingest_AIRS
from roofAI import NAME, VERSION
from abcli import logging
import logging

logger = logging.getLogger(__name__)

NAME = f"{NAME}.ingest"

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "--cache_path",
    type=str,
    default="",
)
parser.add_argument(
    "--ingest_path",
    type=str,
    default="",
)
parser.add_argument(
    "--source",
    type=str,
    default="",
    help="AIRS|TBA",
)
args = parser.parse_args()

success = False
if args.source == "AIRS":
    success = ingest_AIRS(
        args.cache_path,
        args.ingest_path,
    )
else:
    logger.error(f"-{NAME}: {args.task}: {args.source}: source not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
