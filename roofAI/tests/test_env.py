from abcli.tests.test_env import test_abcli_env
from blue_objects.tests.test_env import test_blue_objects_env

from roofAI import env


def test_required_env():
    test_abcli_env()
    test_blue_objects_env()


def test_blue_plugin_env():
    assert env.ROOFAI_TEST_SEMSEG_DATASET
