"""
copied with minor modification from ../../notebooks/semseg.ipynb
"""

import matplotlib.pyplot as plt
import os
from abcli import file, path
import abcli.logging
import logging

logger = logging.getLogger()


# helper function for data visualization
def visualize(
    images,
    filename: str,
    in_notebook: bool = False,
):
    n = len(images)
    plt.figure(figsize=(n * 5, 5))

    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(" ".join(name.split("_")))
        plt.imshow(image)

    plt.subplot(1, n, 1)
    plt.xlabel(path.name(file.path(filename)))

    while file.exist(filename):
        filename = file.add_postfix(filename, "b")
    plt.savefig(filename)
    logger.info(f"-> {filename}")

    if in_notebook:
        plt.show()
    plt.close()
