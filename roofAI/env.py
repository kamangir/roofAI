import os
from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)


ROOFAI_SECRET = os.getenv(
    "ROOFAI_SECRET",
    "",
)

ROOFAI_TEST_SEMSEG_DATASET = os.getenv(
    "ROOFAI_TEST_SEMSEG_DATASET",
    "",
)
