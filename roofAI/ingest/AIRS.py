from abcli import logging
import logging

logger = logging.getLogger(__name__)


def ingest_AIRS(
    cache_path: str,
    ingest_path: str,
    test_count: int = 10,
    train_count: int = 10,
    val_count: int = 10,
) -> bool:
    counts = {
        "test": test_count,
        "train": train_count,
        "val": val_count,
    }

    logger.info(
        "ingesting AIRS -{}-> {} from {}".format(
            " + ".join(
                ["{} X {:,d}".format(subset, count) for subset, count in counts.items()]
            ),
            ingest_path,
            cache_path,
        )
    )

    ...

    return True
