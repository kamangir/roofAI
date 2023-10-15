from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_AIRS(ingest_path: str) -> bool:
    logger.info(f"ingesting AIRS -> {ingest_path}")

    ...

    return True
