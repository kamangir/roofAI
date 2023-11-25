import math
from qgis.core import *
from qgis.gui import *


@qgsfunction(args="auto", group="Custom", referenced_columns=[])
def vanwatch_label(row, webdings, feature, parent):
    """
    Produce label text for a vanwatch mapid.

    vanwatch_label(row)
    """
    row = {
        keyword: value
        for keyword, value in row.items()
        if isinstance(value, int) and value != 0
    }

    scale = {"car": 10, "person": 10}
    symbol = {
        "bicycle": "",
        "car": "",
        "person": "",
    }

    if webdings:
        output = "".join(
            [
                thing
                for thing in [
                    "".join(
                        math.ceil(row.get(thing, 0) / scale.get(thing, 1))
                        * [symbol.get(thing, "x")]
                    )
                    for thing in symbol
                ]
                if thing
            ]
        )
        if not output:
            return output

        side = math.ceil(math.sqrt(len(output)))
        matrix = {0: []}
        j = 0
        for ch in output:
            matrix[j] += [ch]
            if len(matrix[j]) >= side:
                j += 1
                matrix[j] = []
        return "\n".join(["".join(thing) for thing in matrix.values()])

    return ", ".join(sorted([f"{keyword}:{value}" for keyword, value in row.items()]))
