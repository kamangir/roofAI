import os
from roofAI import NAME, VERSION
from abcli import file
from roofAI.logger import logger

CLASSES = [
    "sky",
    "building",
    "pole",
    "road",
    "pavement",
    "tree",
    "signsymbol",
    "fence",
    "car",
    "pedestrian",
    "bicyclist",
    "unlabelled",
]


def ingest_CamVid(ingest_path: str) -> bool:
    logger.info(f"ingesting CamVid -> {ingest_path}")

    return file.save_yaml(
        os.path.join(ingest_path, "metadata.yaml"),
        {
            "classes": CLASSES,
            "kind": "CamVid",
            "source": "CamVid",
            "ingested-by": f"{NAME}-{VERSION}",
        },
        log=True,
    )
