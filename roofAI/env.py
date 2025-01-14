import os
from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)


ROOFAI_SECRET = os.getenv(
    "ROOFAI_SECRET",
    "",
)

TEST_roofAI_ingest_AIRS_v1 = os.getenv(
    "TEST_roofAI_ingest_AIRS_v1",
    "",
)

TEST_roofAI_ingest_AIRS_v2 = os.getenv(
    "TEST_roofAI_ingest_AIRS_v2",
    "",
)

TEST_roofAI_ingest_CamVid_v1 = os.getenv(
    "TEST_roofAI_ingest_CamVid_v1",
    "",
)

TEST_roofAI_semseg_model_AIRS_full_v1 = os.getenv(
    "TEST_roofAI_semseg_model_AIRS_full_v1",
    "",
)

TEST_roofAI_semseg_model_AIRS_full_v2 = os.getenv(
    "TEST_roofAI_semseg_model_AIRS_full_v2",
    "",
)

TEST_roofAI_semseg_model_CamVid_v1 = os.getenv(
    "TEST_roofAI_semseg_model_CamVid_v1",
    "",
)

ROOFAI_AIRS_CACHE_OBJECT_NAME = os.getenv(
    "ROOFAI_AIRS_CACHE_OBJECT_NAME",
    "",
)
