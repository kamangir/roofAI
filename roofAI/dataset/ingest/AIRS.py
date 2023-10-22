import os
from tqdm import tqdm
from abcli import file
from roofAI.dataset import RoofAIDataset, DatasetKind, MatrixKind
from roofAI.semseg.model import chip_width, chip_height
from roofAI import NAME, VERSION
from abcli import string
import numpy as np
from typing import Dict
import matplotlib.pyplot as plt
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
    in_notebook: bool = False,
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

    cache_dataset = RoofAIDataset(cache_path)
    ingest_dataset = RoofAIDataset(
        ingest_path,
        kind=DatasetKind.CAMVID,
    ).create(log=log)

    for subset in tqdm(counts.keys()):
        for matrix_kind in list(MatrixKind):
            chip_count = counts[subset]
            for record_id in cache_dataset.subsets[subset]:
                input_matrix = cache_dataset.get_matrix(
                    subset,
                    record_id,
                    matrix_kind,
                    log=log,
                )

                chip_count -= slice_matrix(
                    input_matrix,
                    matrix_kind,
                    chip_height,
                    chip_width,
                    chip_overlap,
                    max_chip_count=chip_count,
                    output_path=ingest_dataset.subset_path(subset, matrix_kind),
                    prefix=record_id,
                    log=log,
                )

                if chip_count <= 0:
                    break
    file.save_yaml(
        os.path.join(ingest_path, "metadata.yaml"),
        {
            "classes": ingest_dataset.classes,
            "kind": "CamVid",
            "source": "AIRS",
            "ingested-by": f"{NAME}-{VERSION}",
        },
        log=True,
    )

    RoofAIDataset(ingest_path).visualize(
        subset="test",
        index=0,
        in_notebook=in_notebook,
    )

    return True


def slice_matrix(
    input_matrix: np.ndarray,
    kind: MatrixKind,
    chip_height: int,
    chip_width: int,
    chip_overlap: float,
    max_chip_count: int,
    output_path: str,
    prefix: str,
    log: bool = False,
) -> int:
    if log:
        logger.info(
            "slice_matrix[{}]: {} -{}X{}x{}-@{:.0f}%-> {} - {}".format(
                string.pretty_shape_of_matrix(input_matrix),
                kind,
                max_chip_count,
                chip_height,
                chip_width,
                chip_overlap * 100,
                output_path,
                prefix,
            )
        )

    count = 0
    for y in range(
        0, input_matrix.shape[0] - chip_height, int(chip_overlap * chip_height)
    ):
        for x in range(
            0, input_matrix.shape[1] - chip_width, int(chip_overlap * chip_width)
        ):
            count += 1

            chip = input_matrix[
                y : y + chip_height,
                x : x + chip_width,
            ]

            filename = f"{prefix}-{y:05d}-{x:05d}.png"

            assert file.save_image(
                os.path.join(output_path, filename),
                chip,
                log=log,
            )

            if kind == MatrixKind.MASK:
                assert file.save_image(
                    os.path.join(
                        path.parent(output_path),
                        f"{path.name(output_path)}-colored",
                        filename,
                    ),
                    (plt.cm.viridis(chip * 255) * 255).astype(np.uint8)[:, :, :3],
                    log=log,
                )

            if count >= max_chip_count:
                return count

    return count
