import os

from blue_options import MARQUEE as default_MARQUEE
from blue_objects import file, README

from roofAI import NAME, VERSION, ICON, REPO_NAME
from roofAI.dataset.README import items as dataset_items

features = {
    "datasets": {
        "description": "Semantic Segmentation Datasets",
        "icon": ICON,
        "thumbnail": "https://github.com/kamangir/roofAI/raw/main/assets/christchurch_397.png",
        "url": "https://github.com/kamangir/roofAI/blob/main/roofAI/dataset",
    },
    "semseg": {
        "description": "A Semantic Segmenter based on [segmentation_models.pytorch](<https://github.com/qubvel/segmentation_models.pytorch/blob/master/examples/cars%20segmentation%20(camvid).ipynb>).",
        "icon": ICON,
        "thumbnail": "https://github.com/kamangir/roofAI/raw/main/assets/predict-00247.png",
        "url": "https://github.com/kamangir/roofAI/blob/main/roofAI/semseg",
    },
    "template": {
        "description": "",
        "icon": ICON,
        "thumbnail": default_MARQUEE,
        "url": "",
    },
}


items = [
    "{}[`{}`]({}) [![image]({})]({}) {}".format(
        details["icon"],
        feature,
        details["url"],
        details["thumbnail"],
        details["url"],
        details["description"],
    )
    for feature, details in features.items()
    if feature != "template"
]


def build():
    return all(
        [
            README.build(
                items=items,
                path=os.path.join(file.path(__file__), ".."),
                ICON=ICON,
                NAME=NAME,
                VERSION=VERSION,
                REPO_NAME=REPO_NAME,
            ),
            README.build(
                items=dataset_items,
                cols=len(dataset_items),
                path=os.path.join(file.path(__file__), "dataset"),
                ICON=ICON,
                NAME=NAME,
                VERSION=VERSION,
                REPO_NAME=REPO_NAME,
            ),
        ]
    )
