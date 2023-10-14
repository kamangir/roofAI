from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_AIRS(
    cache_path: str,
    ingest_path: str,
) -> bool:
    logger.info(f"ingesting AIRS: {cache_path} -> {ingest_path}")

    ...

    return True
