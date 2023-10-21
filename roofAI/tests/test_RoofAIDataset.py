import pytest
import os
from abcli.modules import objects
from roofAI.dataset import RoofAIDataset, MatrixKind, DatasetKind
from abcli.plugins import cache
import numpy as np


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
    matrix_kind,
    dataset_kind,
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
            "roofAI_ingest_CamVid_v1",
            "RoofAIDataset[DatasetKind.CAMVID:CamVid](",
            "test",
            10,
            MatrixKind.IMAGE,
            "test/0001TP_009390.png",
            (360, 480, 3),
        ),
        (
            "roofAI_ingest_CamVid_v1",
            "RoofAIDataset[DatasetKind.CAMVID:CamVid](",
            "test",
            10,
            MatrixKind.MASK,
            "testannot/0001TP_009390.png",
            (360, 480),
        ),
        (
            "roofAI_ingest_AIRS_cache",
            "RoofAIDataset[DatasetKind.AIRS:AIRS](",
            "test",
            10,
            MatrixKind.IMAGE,
            "test/image/christchurch_585.tif",
            (10000, 10000, 3),
        ),
        (
            "roofAI_ingest_AIRS_cache",
            "RoofAIDataset[DatasetKind.AIRS:AIRS](",
            "test",
            10,
            MatrixKind.MASK,
            "test/label/christchurch_585.tif",
            (10000, 10000),
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
    dataset = RoofAIDataset(objects.object_path(cache.read(dataset_object_name)))

    assert dataset.one_liner.startswith(one_liner_prefix)

    assert dataset.dataset_path

    record_id = dataset.subsets[subset][index]
    assert record_id

    filename = dataset.get_filename(subset, record_id, matrix_kind, log=True)
    assert filename == os.path.join(dataset.dataset_path, expected_filename)

    matrix = dataset.get_matrix(subset, record_id, matrix_kind, log=True)
    assert matrix.shape == expected_shape
    assert matrix.dtype == np.uint8
