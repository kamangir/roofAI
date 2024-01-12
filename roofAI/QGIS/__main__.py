import argparse
from roofAI.QGIS import NAME
from roofAI import VERSION
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
    list_of_files = ["seed.py"]  # TODO: add the rest of the files
    seed = "; ".join(
        [
            'exec(Path(f\'{os.getenv("HOME")}/git/roofAI/roofAI/QGIS/console/'
            + filename
            + "').read_text())"
            for filename in list_of_files
        ]
    )
    print(seed)
    success = True
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
