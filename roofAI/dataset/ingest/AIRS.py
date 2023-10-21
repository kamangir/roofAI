from typing import Dict
from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_AIRS(
    cache_path: str,
    ingest_path: str,
    counts: Dict[str, int],
) -> bool:
    logger.info(
        "ingesting AIRS -{}-> {} from {}".format(
            " + ".join(
                ["{} X {:,d}".format(subset, count) for subset, count in counts.items()]
            ),
            ingest_path,
            cache_path,
        )
    )

    logger.info("wip")

    return True
