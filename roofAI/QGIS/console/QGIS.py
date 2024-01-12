from init import NAME, VERSION
from layer import ABCLI_QGIS_Layer
from project import ABCLI_QGIS_Project


class ABCLI_QGIS(object):
    def __init__(self):
        self.layer = ABCLI_QGIS_Layer()
        self.project = ABCLI_QGIS_Project()
        self.app_list = []
        self.verbose = False
        self.object_name = self.timestamp()

    def add_application(self, app):
        self.app_list += [app]

    def intro(self):
        self.log(
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
        self.log(f"Type in Q.help() for help.")

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

    def create_video(self, filename="QGIS", object_name=""):
        self.seed(
            "abcli create_video png,fps=2,filename={},gif {}".format(
                filename, object_name if object_name else self.object_name
            )
        )

    def export(self, filename="", object_name=""):
        filename = self.file_path(
            filename=filename if filename else "{}.png".format(self.timestamp()),
            object_name=object_name,
        )

        qgis.utils.iface.mapCanvas().saveAsImage(filename)
        self.log(filename, icon="🖼️")

    def file_path(self, filename, object_name=""):
        return os.path.join(self.object_path(object_name), filename)

    def find_layer(self, layer_name):
        return QgsProject.instance().mapLayersByName(layer_name)

    def help(self):
        self.log("📂 object", self.object_name)
        self.log("Q.clear()", "clear Python Console.")
        self.log("Q.create_video()", "create a video.")
        self.layer.help()
        if self.verbose:
            self.log("Q.export([filename],[object_name])", "export.")
            self.log("Q.list_of_layers()", "list of layers.")
            self.log("Q.load(filename,layer_name,template_name)", "load a layer.")
        self.log('Q.open("|<object-name>|layer|object|project")', "upload.")
        self.project.help()
        if self.verbose:
            self.log("Q.refresh()", "refresh.")
            self.log("Q.reload()", "reload all layers.")
        self.log('Q.select("<object-name>")', "select <object-name>.")
        if self.verbose:
            self.log("Q.unload(layer_name)", "unload layer_name.")
        self.log('Q.upload("|<object-name>|layer|project")', "upload.")
        self.log("Q.verbose=True|False", "set verbose state.")

        for app in self.app_list:
            app.help()

    def list_of_layers(self, aux=False):
        output = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        if not aux:
            output = [
                layer_name
                for layer_name in output
                if not layer_name.startswith("Google")
                and not layer_name.startswith("template")
            ]
        self.log(
            "{} layer(s){}".format(
                len(output),
                ": {}".format(", ".join(output)) if self.verbose else "",
            ),
            icon="🔎",
        )
        return output

    def load(
        self,
        filename,
        layer_name,
        template_name="",
        refresh=True,
    ):
        if len(QGIS.find_layer(layer_name)) > 0:
            print(f"✅ {layer_name}")
            return True

        if filename.endswith(".geojson"):
            layer_ = QgsVectorLayer(filename, layer_name, "ogr")
        elif filename.endswith(".tif"):
            layer_ = QgsRasterLayer(filename, layer_name)
        else:
            self.log_error(f"cannot load {filename}.")
            return False

        if not layer_.isValid():
            QGIS.log_error(f"invalid layer: {filename}.")
            return False

        QgsProject.instance().addMapLayer(layer_)

        if template_name:
            template_layer = QGIS.find_layer(template_name)
            if not len(template_layer):
                QGIS.log_error(f"template not found: {template_name}.")
                return False

            # https://gis.stackexchange.com/a/357206/210095
            source_style = QgsMapLayerStyle()
            source_style.readFromLayer(template_layer[0])
            source_style.writeToLayer(layer_)
            layer_.triggerRepaint()

        self.log(
            layer_name,
            template_name if self.verbose else "",
            icon="🎨",
        )

        if refresh:
            QGIS.refresh()

    def log(self, message, note="", icon="🌐"):
        print(
            "{} {}{}".format(
                icon,
                f"{message:.<40}" if note else message,
                note,
            )
        )

    def log_error(self, message, note=""):
        self.log(message, note, icon="❗️")

    def object_path(self, object_name=""):
        output = os.path.join(
            abcli_object_root,
            object_name if object_name else self.object_name,
        )
        os.makedirs(output, exist_ok=True)
        return output

    def open(self, what="object"):
        self.open_folder(
            layer.path
            if what == "layer"
            else self.object_path()
            if what == "object"
            else project.path
        )

    def open_folder(self, path):
        if not path:
            self.log_error("path not found.")
            return

        self.log(path)
        os.system(f"open {path}")

    def refresh(self, deep=False):
        self.log("{}refresh.".format("deep" if deep else ""))
        if deep:
            # https://api.qgis.org/api/classQgsMapCanvas.html
            iface.mapCanvas().redrawAllLayers()
        else:
            iface.mapCanvas().refresh()

    def reload(self):
        # https://gis.stackexchange.com/a/449101/210095
        for layer_ in tqdm(QgsProject.instance().mapLayers().values()):
            layer_.dataProvider().reloadData()

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

        self.log(hash_id, command, icon="🌱")

    def select(self, object_name=""):
        self.object_name = object_name if object_name else QGIS.timestamp()
        self.log("📂 object_name", self.object_name)
        self.log("📂 object_path", self.object_path())

        os.makedirs(self.object_path(), exist_ok=True)

    def timestamp(self):
        return time.strftime(
            f"%Y-%m-%d-%H-%M-%S-{random.randrange(100000):05d}",
            time.localtime(time.time()),
        )

    def unload(self, layer_name, refresh=True):
        self.log(layer_name, icon="🗑️")

        for layer_ in self.find_layer(layer_name):
            QgsProject.instance().removeMapLayer(layer_.id())

        if refresh:
            QGIS.refresh()

    def upload(self, object_name=""):
        self.seed(
            "abcli upload - {}".format(
                project.name
                if object_name == "project"
                else layer.object_name
                if object_name == "layer"
                else object_name
                if object_name
                else self.object_name
            )
        )
