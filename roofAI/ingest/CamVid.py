import os
from roofAI.semseg.dataloader import Dataset
from roofAI import NAME, VERSION
from abcli import file
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_CamVid(ingest_path: str) -> bool:
    logger.info(f"ingesting CamVid -> {ingest_path}")

    return file.save_yaml(
        os.path.join(ingest_path, "metadata.yaml"),
        {
            "classes": Dataset.CLASSES,
            "path_prefix": "SegNet-Tutorial/CamVid",
            "source": "CamVid",
            "ingested-by": f"{NAME}-{VERSION}",
        },
        log=True,
    )
