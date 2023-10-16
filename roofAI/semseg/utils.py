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
    plt.figure(figsize=(n * 5, 5))

    for name in images:
        if isinstance(images[name], str):
            success, images[name] = file.load_image(images[name], log=True)
            assert success

    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
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
        plt.imshow(image)

    plt.subplot(1, n, 1)

    plt.title(
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
        while file.exist(filename):
            filename = file.add_postfix(filename, "b")
        plt.savefig(filename)
        logger.info(f"-> {filename}")

    if in_notebook:
        plt.show()
    plt.close()
