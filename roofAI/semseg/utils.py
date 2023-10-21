"""
copied with minor modification from ../../notebooks/semseg.ipynb
"""

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from abcli import file
from abcli import path
from abcli import string
from typing import List
import abcli.logging
import logging

logger = logging.getLogger()


# helper function for data visualization
def visualize(
    images,
    filename: str = "",
    in_notebook: bool = False,
    description: List[str] = [],
):
    n = len(images)
    fig = plt.figure(figsize=(n * 5, 5))

    for name in images:
        if isinstance(images[name], str):
            success, images[name] = image = file.load_image(images[name], log=True)
            assert success

    for name in images:
        images[name][np.isnan(images[name])] = 0

    for i, (name, image) in enumerate(images.items()):
        ax = fig.add_subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(
            "{} - {}{}".format(
                name,
                string.pretty_shape_of_matrix(image),
                " - {} levels: {}..{}".format(
                    len(np.unique(image)),
                    int(np.min(image)),
                    int(np.max(image)),
                )
                if name in "prediction,mask,groundtruth".split(",")
                else "",
            )
        )
        ax.imshow(image)

    # https://stackoverflow.com/a/7066293/17619982
    fig.suptitle(
        " | ".join(
            [
                thing
                for thing in [
                    path.name(file.path(filename)),
                ]
                + description
                if thing
            ]
        )
    )

    if filename:
        file.prepare_for_saving(filename)
        plt.savefig(filename)
        logger.info(f"-> {filename}")

    if in_notebook:
        plt.show()
    plt.close()
