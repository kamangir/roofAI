import pytest
import os
import numpy as np

from blue_objects import objects

from roofai.env import TEST_roofAI_ingest_CamVid_v1
from roofai.dataset.classes import RoofAIDataset, MatrixKind, DatasetKind


@pytest.mark.parametrize(
    "dataset_kind, matrix_kind, subset_path, filename_and_extension",
    [
        (
            DatasetKind.AIRS,
            MatrixKind.IMAGE,
            "subset/image",
            "subset/image/record_id.tif",
        ),
        (
            DatasetKind.AIRS,
            MatrixKind.MASK,
            "subset/label",
            "subset/label/record_id.tif",
        ),
        (
            DatasetKind.CAMVID,
            MatrixKind.IMAGE,
            "subset",
            "subset/record_id.png",
        ),
        (
            DatasetKind.CAMVID,
            MatrixKind.MASK,
            "subsetannot",
            "subsetannot/record_id.png",
        ),
    ],
)
def test_MatrixKind(
    dataset_kind: DatasetKind,
    matrix_kind: MatrixKind,
    subset_path,
    filename_and_extension,
):
    assert matrix_kind.subset_path(dataset_kind, "subset") == subset_path

    assert (
        matrix_kind.filename_and_extension(dataset_kind, "subset", "record_id")
        == filename_and_extension
    )


@pytest.mark.parametrize(
    "dataset_object_name, one_liner_prefix, subset, index, matrix_kind, expected_filename, expected_shape",
    [
        (
            TEST_roofAI_ingest_CamVid_v1,
            "RoofAIDataset[kind:DatasetKind.CAMVID,source:CamVid](",
            "test",
            10,
            MatrixKind.IMAGE,
            "test/0001TP_008850.png",
            (360, 480, 3),
        ),
        (
            TEST_roofAI_ingest_CamVid_v1,
            "RoofAIDataset[kind:DatasetKind.CAMVID,source:CamVid](",
            "test",
            10,
            MatrixKind.MASK,
            "testannot/0001TP_008850.png",
            (360, 480),
        ),
        (
            "palisades-dataset-v1",
            "RoofAIDataset[kind:DatasetKind.DISTRIBUTED,source:catalog_query](",
            "train",
            0,
            MatrixKind.IMAGE,
            "datacube-maxar_open_data-WildFires-LosAngeles-Jan-2025-11-031311102213-103001010B9A1B00/11-031311102213-103001010B9A1B00-103001010B9A1B00-visual.tif",
            (17408, 17408, 3),
        ),
        (
            "palisades-dataset-v1",
            "RoofAIDataset[kind:DatasetKind.DISTRIBUTED,source:catalog_query](",
            "train",
            0,
            MatrixKind.MASK,
            "datacube-maxar_open_data-WildFires-LosAngeles-Jan-2025-11-031311102213-103001010B9A1B00/11-031311102213-103001010B9A1B00-103001010B9A1B00-visual-label.tif",
            (17408, 17408),
        ),
    ],
)
def test_RoofAIDataset(
    dataset_object_name,
    one_liner_prefix,
    subset,
    index,
    matrix_kind,
    expected_filename,
    expected_shape,
):
    assert objects.download(dataset_object_name)

    dataset = RoofAIDataset(objects.object_path(dataset_object_name))

    assert dataset.one_liner.startswith(one_liner_prefix)

    assert dataset.dataset_path

    record_id = dataset.subsets[subset][index]
    assert record_id

    filename = dataset.get_filename(subset, record_id, matrix_kind, log=True)
    if dataset.kind == DatasetKind.DISTRIBUTED:
        assert filename.endswith(expected_filename)
    else:
        assert filename == os.path.join(dataset.dataset_path, expected_filename)

    matrix = dataset.get_matrix(subset, record_id, matrix_kind, log=True)
    assert matrix.shape == expected_shape
    assert matrix.dtype == np.uint8
