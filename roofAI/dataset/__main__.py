import argparse
from tqdm import trange
from roofAI import VERSION
from roofAI.dataset import NAME
from roofAI.dataset.classes import RoofAIDataset
from roofAI.dataset.classes import DatasetTarget
from roofAI.dataset.ingest.AIRS import ingest_AIRS
from roofAI.dataset.ingest.CamVid import ingest_CamVid
from roofAI.logger import logger
from blueness.argparse.generic import ending


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
    "--log",
    type=int,
    default=1,
    help="0|1",
)
parser.add_argument(
    "--verbose",
    type=int,
    default=0,
    help="0|1",
)
parser.add_argument(
    "--source",
    type=str,
    default="",
    help="AIRS|CamVid",
)
parser.add_argument(
    "--target",
    type=str,
    default="torch",
    help="torch|sagemaker",
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
            cache_path=args.cache_path,
            ingest_path=args.ingest_path,
            counts={
                "test": args.test_count,
                "train": args.train_count,
                "val": args.val_count,
            },
            target=DatasetTarget[args.target.upper()],
            log=args.log,
            verbose=args.verbose,
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
            log=args.log,
        )

    success = True
else:
    success = None

ending(logger, NAME, args.task, success)
