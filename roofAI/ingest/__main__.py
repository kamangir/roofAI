import argparse
from roofAI.ingest.AIRS import ingest_AIRS
from roofAI.ingest.CamVid import ingest_CamVid
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
    help="AIRS|CamVid",
)
parser.add_argument(
    "--test_count",
    type=int,
    default="10",
)
parser.add_argument(
    "--train_count",
    type=int,
    default="10",
)
parser.add_argument(
    "--val_count",
    type=int,
    default="10",
)
args = parser.parse_args()

success = False
if args.source == "AIRS":
    success = ingest_AIRS(
        args.cache_path,
        args.ingest_path,
        test_count=args.test_count,
        train_count=args.train_count,
        val_count=args.val_count,
    )
elif args.source == "CamVid":
    success = ingest_CamVid(args.ingest_path)
else:
    logger.error(f"-{NAME}: {args.task}: {args.source}: source not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
