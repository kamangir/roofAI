# meant to be run inside Python Console in QGIS.
# run `QGIS seed` 🌱 to start.

import time
import random
import os
from tqdm import tqdm
import glob

# TODO: if not in a seed
from application import ABCLI_QGIS_APPLICATION
from layer import ABCLI_QGIS_Layer
from project import ABCLI_QGIS_Project


QGIS = ABCLI_QGIS()

Q = QGIS
layer = QGIS.layer
project = QGIS.project

vanwatch = ABCLI_QGIS_APPLICATION_VANWATCH()
QGIS.add_application(vanwatch)

QGIS.intro()
