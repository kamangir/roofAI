import os
from tqdm import tqdm
from typing import List, Tuple
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
        record_id_list = []
        for matrix_kind in [MatrixKind.MASK, MatrixKind.IMAGE]:  # order is critical.
            chip_count = counts[subset]
            for record_id in cache_dataset.subsets[subset]:
                input_matrix = cache_dataset.get_matrix(
                    subset,
                    record_id,
                    matrix_kind,
                    log=log,
                )

                slice_count, slice_record_id_list = slice_matrix(
                    input_matrix=input_matrix,
                    kind=matrix_kind,
                    chip_height=chip_height,
                    chip_width=chip_width,
                    chip_overlap=chip_overlap,
                    max_chip_count=chip_count,
                    record_id_list=record_id_list,
                    output_path=ingest_dataset.subset_path(subset, matrix_kind),
                    prefix=record_id,
                    log=False,
                )
                chip_count -= slice_count
                record_id_list = list(set(record_id_list + slice_record_id_list))

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
    record_id_list: List[str],
    output_path: str,
    prefix: str,
    log: bool = False,
) -> Tuple[int, List[str]]:
    if log:
        logger.info(
            "slice_matrix[{}]: {} -{}X{}x{}-@{:.0f}%-> {} - {}{}".format(
                string.pretty_shape_of_matrix(input_matrix),
                kind,
                max_chip_count,
                chip_height,
                chip_width,
                chip_overlap * 100,
                output_path,
                prefix,
                ""
                if kind == MatrixKind.MASK
                else ": {} record_id(s): {}".format(
                    len(record_id_list),
                    ", ".join(record_id_list[:3] + ["..."]),
                ),
            )
        )

    record_id_list_output = []

    count = 0
    for y in range(
        0, input_matrix.shape[0] - chip_height, int(chip_overlap * chip_height)
    ):
        for x in range(
            0, input_matrix.shape[1] - chip_width, int(chip_overlap * chip_width)
        ):
            chip = input_matrix[
                y : y + chip_height,
                x : x + chip_width,
            ]

            record_id = f"{prefix}-{y:05d}-{x:05d}"

            # to ensure variety of labels in the pixel.
            # TODO: make it more elaborate.
            if (kind == MatrixKind.MASK and (len(np.unique(chip)) < 2)) or (
                kind == MatrixKind.IMAGE and (record_id not in record_id_list)
            ):
                continue
            record_id_list_output += [record_id]

            assert file.save_image(
                os.path.join(output_path, f"{record_id}.png"),
                chip,
                log=log,
            )

            if kind == MatrixKind.MASK:
                assert file.save_image(
                    os.path.join(
                        path.parent(output_path),
                        f"{path.name(output_path)}-colored",
                        f"{record_id}.png",
                    ),
                    (plt.cm.viridis(chip * 255) * 255).astype(np.uint8)[:, :, :3],
                    log=log,
                )

            count += 1
            if count >= max_chip_count:
                return count, record_id_list_output

    return count, record_id_list_output
