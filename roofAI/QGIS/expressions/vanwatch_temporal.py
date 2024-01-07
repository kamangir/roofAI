import os
from qgis.core import *
from qgis.gui import *


@qgsfunction(args="auto", group="Custom", referenced_columns=[])
def vanwatch_temporal(layer_name, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
    </ul>
    """
    HOME = os.getenv("HOME", "")
    abcli_QGIS_path_cache = os.path.join(HOME, "git/vancouver-watching/QGIS")

    list_of_layers = []
    for _, _, files in os.walk(abcli_QGIS_path_cache):
        for filename in files:
            if filename.endswith(".geojson"):
                list_of_layers += [filename.split(".")[0]]

    list_of_layers = sorted(list_of_layers)

    if layer_name not in list_of_layers:
        return ""

    index = list_of_layers.index(layer_name)

    return list_of_layers[index + 1] if index < len(list_of_layers) - 1 else ""
