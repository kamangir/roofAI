"""
copied with minor modification from ../../notebooks/semseg.ipynb
"""

import matplotlib.pyplot as plt
import cv2
import os
from abcli import file
from abcli import path
from abcli import string
import abcli.logging
import logging

logger = logging.getLogger()


# helper function for data visualization
def visualize(
    images,
    filename: str = "",
    in_notebook: bool = False,
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
        plt.title(
            "{} - {}".format(
                name.replace("_", " "),
                string.pretty_shape_of_matrix(image),
            )
        )
        plt.imshow(image)

    plt.subplot(1, n, 1)

    if filename:
        plt.xlabel(path.name(file.path(filename)))

        while file.exist(filename):
            filename = file.add_postfix(filename, "b")
        plt.savefig(filename)
        logger.info(f"-> {filename}")

    if in_notebook:
        plt.show()
    plt.close()
