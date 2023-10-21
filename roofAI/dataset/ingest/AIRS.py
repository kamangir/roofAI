from typing import Dict
from abcli import path
from roofAI.semseg.model import chip_width, chip_height
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_AIRS(
    cache_path: str,
    ingest_path: str,
    counts: Dict[str, int],
    chip_height: int = chip_height,
    chip_width: int = chip_width,
    chip_overlap: float = 0.5,
    log: bool = False,
) -> bool:
    logger.info(
        "ingesting AIRS {} -{}-{}x{}-@{:.0f}%-> {}".format(
            path.name(cache_path),
            " + ".join(
                ["{} X {:,d}".format(subset, count) for subset, count in counts.items()]
            ),
            chip_height,
            chip_width,
            chip_overlap * 100,
            path.name(ingest_path),
        )
    )

    logger.info("wip")

    return True
