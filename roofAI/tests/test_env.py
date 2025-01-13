from abcli.tests.test_env import test_abcli_env
from blue_objects.tests.test_env import test_blue_objects_env
from blue_objects.env import ABCLI_MLFLOW_EXPERIMENT_PREFIX

from roofAI import env


def test_required_env():
    test_abcli_env()
    test_blue_objects_env()


def test_blue_plugin_env():
    assert env.ROOFAI_TEST_SEMSEG_DATASET


def test_debug():
    assert (
        ABCLI_MLFLOW_EXPERIMENT_PREFIX == "/Users/kamangirblog@gmail.com/"
    ), ABCLI_MLFLOW_EXPERIMENT_PREFIX
