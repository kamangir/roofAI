from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from roofAI import ALIAS
from roofAI.help.dataset import help_functions as help_dataset


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "dataset": help_dataset,
    }
)
