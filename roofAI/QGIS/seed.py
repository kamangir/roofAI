# meant to be run inside Python Console in QGIS.
# run `QGIS seed 🌱` to start.

import os
from tqdm import tqdm

NAME = "roofAI.QGIS"

VERSION = "4.15.1"


abcli_object_root = os.path.join(
    os.getenv("HOME", ""),
    "storage/abcli",
)


class ABCLI_QGIS_Layer(object):
    def help(self):
        log("Q.layer.open()", "open layer.")

    @property
    def filename(self):
        try:
            return iface.activeLayer().dataProvider().dataSourceUri()
        except:
            log_error("unknown layer.filename.")
            return ""

    @property
    def name(self):
        filename = self.filename
        return filename.split(os.sep)[-1].split(".")[0] if filename else ""

    @property
    def object_name(self):
        filename = self.filename
        return filename.split(os.sep)[-2] if filename else ""

    def open(self):
        open_folder(self.path)

    @property
    def path(self):
        return os.path.dirname(self.filename)


class ABCLI_QGIS_Project(object):
    def help(self):
        log("Q.project.open()", "open project.")

    @property
    def name(self):
        return QgsProject.instance().homePath().split(os.sep)[-1]

    def open(self):
        open_folder(self.path)

    @property
    def path(self):
        return QgsProject.instance().homePath()


class ABCLI_QGIS(object):
    def __init__(self):
        self.layer = ABCLI_QGIS_Layer()
        self.project = ABCLI_QGIS_Project()

    def intro(self):
        log(f"{NAME}-{VERSION} initialized.")
        log(f"Type in Q.help() for help.")

    @property
    def l(self):
        return self.layer

    @property
    def p(self):
        return self.project

    def clear(self):
        # https://gis.stackexchange.com/a/216444/210095
        from qgis.PyQt.QtWidgets import QDockWidget

        consoleWidget = iface.mainWindow().findChild(QDockWidget, "PythonConsole")
        consoleWidget.console.shellOut.clearConsole()

        self.intro()

    def help(self):
        log("Q.clear()", "clear Python Console.")

        self.layer.help()
        self.project.help()

        log("Q.reload()", "reload all layers.")

    def reload(self):
        # https://gis.stackexchange.com/a/449101/210095
        for layer in tqdm(QgsProject.instance().mapLayers().values()):
            layer.dataProvider().reloadData()


def log(message, note="", error=False):
    print(
        "{} {}{}".format(
            "❗️" if error else "🌐",
            f"{message:.<20}" if note else message,
            note,
        )
    )


def log_error(message, note=""):
    log(message, note, error=True)


def open_folder(path):
    if not path:
        log_error("path not found.")
        return

    log(path)
    os.system(f"open {path}")


QGIS = ABCLI_QGIS()
QGIS.intro()

Q = QGIS
layer = QGIS.layer
project = QGIS.project
