import argparse
from roofAI.dataset.ingest.AIRS import ingest_AIRS
from roofAI.dataset.ingest.CamVid import ingest_CamVid
from tqdm import trange
from roofAI.dataset import RoofAIDataset
from abcli.modules import objects
from roofAI import NAME, VERSION
from abcli import logging
import logging

logger = logging.getLogger(__name__)

NAME = f"{NAME}.dataset"

parser = argparse.ArgumentParser(
    f"python3 -m {NAME}",
    description=f"{NAME}-{VERSION}",
)
parser.add_argument(
    "task",
    type=str,
    help="ingest|review",
)
parser.add_argument(
    "--cache_path",
    type=str,
    default="",
)
parser.add_argument(
    "--count",
    type=int,
    default=1,
)
parser.add_argument(
    "--dataset_path",
    type=str,
    default="",
)
parser.add_argument(
    "--description",
    type=str,
    help="line1,line2",
    default="",
)
parser.add_argument(
    "--index",
    type=int,
    default=10,
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
    "--subset",
    type=str,
    default="test",
)
parser.add_argument(
    "--test_count",
    type=int,
    default=10,
)
parser.add_argument(
    "--train_count",
    type=int,
    default=10,
)
parser.add_argument(
    "--val_count",
    type=int,
    default=10,
)
args = parser.parse_args()

success = False
if args.task == "ingest":
    if args.source == "AIRS":
        success = ingest_AIRS(
            args.cache_path,
            args.ingest_path,
            {
                "test": args.test_count,
                "train": args.train_count,
                "val": args.val_count,
            },
        )
    elif args.source == "CamVid":
        success = ingest_CamVid(args.ingest_path)
    else:
        logger.error(f"-{NAME}: {args.task}: {args.source}: source not found.")
elif args.task == "review":
    dataset = RoofAIDataset(args.dataset_path)

    for index in trange(args.count):
        dataset.visualize(
            subset=args.subset,
            index=index + args.index,
            in_notebook=False,
            description=args.description.split(","),
            log=True,
        )

    success = True
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")