import os

from blue_options import MARQUEE as default_MARQUEE
from blue_objects import file, README

from roofAI import NAME, VERSION, ICON, REPO_NAME

features = {
    "semseg": {
        "description": "A Semantic Segmenter based on [segmentation_models.pytorch](<https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb>).",
        "icon": ICON,
        "thumbnail": "https://github.com/kamangir/roofAI/raw/refactors-2025-01-12-F7jvKo/assets/predict-00247.png",
        "url": "https://github.com/kamangir/roofAI/blob/main/roofAI/semseg",
    },
    "datasets": {
        "description": "Relevant Datasets",
        "icon": ICON,
        "thumbnail": "https://github.com/kamangir/roofAI/raw/refactors-2025-01-12-F7jvKo/assets/christchurch_397.png",
        "url": "https://github.com/kamangir/roofAI/blob/main/roofAI/dataset",
    },
    "template": {
        "description": "",
        "icon": ICON,
        "thumbnail": default_MARQUEE,
        "url": "",
    },
}


items = [
    "{}[`{}`](#) [![image]({})](#) {}".format(
        ICON,
        f"feature {index}",
        "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true",
        f"description of feature {index} ...",
    )
    for index in range(1, 4)
]


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
