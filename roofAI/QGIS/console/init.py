import os

NAME = "roofAI.QGIS"

VERSION = "5.2.1"

HOME = os.getenv("HOME", "")
abcli_object_root = os.path.join(HOME, "storage/abcli")
abcli_QGIS_path_shared = os.path.join(HOME, "Downloads/QGIS")
abcli_QGIS_path_server = os.path.join(abcli_QGIS_path_shared, "server")

os.makedirs(abcli_QGIS_path_server, exist_ok=True)
