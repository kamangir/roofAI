# meant to be run inside Python Console in QGIS.
# run `QGIS seed 🌱` to start.

import os
import re
from pathlib import Path
from typing import Any, Dict, List

import pyperclip
import yaml
from tqdm import tqdm

NAME = "roofAI.QGIS"

VERSION = "3.14.1"


abcli_object_root = os.path.join(
    os.getenv("HOME", ""),
    "storage/abcli",
)


class ABCLI_QGIS_Layer(object):
    @property
    def help(self):
        log("QGIS.layer.name", self.name)
        log("QGIS.layer.object", self.object)
        log("QGIS.layer.open")
        log("QGIS.layer.path", self.path)

    @property
    def name(self):
        output = ""
        try:
            output = (
                iface.activeLayer()
                .dataProvider()
                .dataSourceUri()
                .split(os.sep)[-1]
                .split(".")[0]
            )
        except:
            log_error("no layer is selected.")

        return output

    @property
    def object(self):
        output = ""
        try:
            output = (
                iface.activeLayer().dataProvider().dataSourceUri().split(os.sep)[-2]
            )
        except:
            log_error("no layer is selected.")

        return output

    @property
    def open(self):
        open_folder(self.path)

    @property
    def path(self):
        output = ""
        try:
            output = os.path.dirname(iface.activeLayer().dataProvider().dataSourceUri())
        except:
            log_error("no layer is selected.")

        return output


class ABCLI_QGIS_Project(object):
    @property
    def all(self):
        return self.help

    @property
    def help(self):
        log("QGIS.project.name", self.name)
        log("QGIS.project.path", self.path)
        log("QGIS.project.open")

    @property
    def name(self):
        return QgsProject.instance().homePath().split(os.sep)[-1]

    @property
    def open(self):
        open_folder(self.path)

    @property
    def path(self):
        return QgsProject.instance().homePath()


class ABCLI_QGIS(object):
    def __init__(self):
        self.layer = ABCLI_QGIS_Layer()
        self.project = ABCLI_QGIS_Project()

        self.list_of_apps: List[Any] = []

    @property
    def intro(self):
        log(f"{NAME}-{VERSION} initialized.")

    @property
    def l(self):
        return self.layer

    @property
    def p(self):
        return self.project

    @property
    def clear(self):
        # https://gis.stackexchange.com/a/216444/210095
        from qgis.PyQt.QtWidgets import QDockWidget

        consoleWidget = iface.mainWindow().findChild(QDockWidget, "PythonConsole")
        consoleWidget.console.shellOut.clearConsole()

        self.intro

    @property
    def help(self):
        log("QGIS.clear", "clear Python Console.")

        self.layer.help
        self.project.help

        log("QGIS.reload", "reload all layers.")


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
Q = QGIS

QGIS.clear
