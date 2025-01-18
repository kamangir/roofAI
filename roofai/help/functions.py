from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from roofai import ALIAS
from roofai.help.dataset import help_functions as help_dataset
from roofai.help.semseg import help_functions as help_semseg


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "dataset": help_dataset,
        "semseg": help_semseg,
    }
)
