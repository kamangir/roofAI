# meant to be run inside Python Console in QGIS.
# run `QGIS seed 🌱` to start.

import time
import random
import os
from tqdm import tqdm
import glob

NAME = "roofAI.QGIS"

VERSION = "4.37.1"


HOME = os.getenv("HOME", "")
abcli_object_root = os.path.join(HOME, "storage/abcli")
abcli_QGIS_path_cache = os.path.join(HOME, "git/vancouver-watching/QGIS")
abcli_QGIS_path_shared = os.path.join(HOME, "Downloads/QGIS")
abcli_QGIS_path_server = os.path.join(abcli_QGIS_path_shared, "server")

os.makedirs(abcli_QGIS_path_server, exist_ok=True)


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


class ABCLI_QGIS_APPLICATION(object):
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        log(self.name, "", icon=self.icon)

    def log(self, message, note=""):
        log(message, note, icon=self.icon)


class ABCLI_QGIS_APPLICATION_VANWATCH(ABCLI_QGIS_APPLICATION):
    def __init__(self):
        super().__init__("vanwatch", "🌈")

    def help(self):
        self.log("vanwatch.ingest()", "ingest a layer now.")
        self.log("vanwatch.list()", "list vanwatch layers.")

    def ingest(self):
        QGIS.seed("abcli_aws_batch source - vanwatch/ingest - count=-1,publish")

    def list(self):
        return [
            os.path.splitext(os.path.basename(filename))[0]
            for filename in glob.glob(
                os.path.join(
                    abcli_QGIS_path_cache,
                    "*.geojson",
                )
            )
        ]


class ABCLI_QGIS(object):
    def __init__(self):
        self.layer = ABCLI_QGIS_Layer()
        self.project = ABCLI_QGIS_Project()
        self.app_list = []

    def add_application(self, app):
        self.app_list += [app]

    def intro(self):
        log(
            "{}-{}: {}".format(
                NAME,
                VERSION,
                ", ".join(
                    [
                        "{} {}".format(
                            app.name,
                            app.icon,
                        )
                        for app in self.app_list
                    ]
                ),
            )
        )
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

        for app in self.app_list:
            app.help()

    def reload(self):
        # https://gis.stackexchange.com/a/449101/210095
        for layer in tqdm(QgsProject.instance().mapLayers().values()):
            layer.dataProvider().reloadData()

    def seed(self, command):
        hash_id = "{}-{:05d}".format(
            time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())),
            random.randrange(100000),
        )
        with open(
            os.path.join(
                abcli_QGIS_path_server,
                f"{hash_id}.command",
            ),
            "w",
        ) as f:
            f.write(command)

        log(hash_id, command, icon="🌱")


def log(message, note="", icon="🌐"):
    print(
        "{} {}{}".format(
            icon,
            f"{message:.<32}" if note else message,
            note,
        )
    )


def log_error(message, note=""):
    log(message, note, icon="❗️")


def open_folder(path):
    if not path:
        log_error("path not found.")
        return

    log(path)
    os.system(f"open {path}")


QGIS = ABCLI_QGIS()

Q = QGIS
layer = QGIS.layer
project = QGIS.project

vanwatch = ABCLI_QGIS_APPLICATION_VANWATCH()
QGIS.add_application(vanwatch)

QGIS.intro()
