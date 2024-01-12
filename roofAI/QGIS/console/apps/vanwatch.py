import os
import glob
from application import ROOFAI_QGIS_APPLICATION
from log import log
from project import project
from QGIS import QGIS
from seed import seed


class ROOFAI_QGIS_APPLICATION_VANWATCH(ROOFAI_QGIS_APPLICATION):
    def __init__(self):
        super().__init__("vanwatch", "🌈")

    def help(self):
        self.log("vanwatch.ingest()", "ingest a layer now.")
        self.log("vanwatch.list_layers()", "list vanwatch layers.")
        self.log("vanwatch.load([prefix], [count])", "load layers.")
        self.log("vanwatch.unload(prefix)", "unload prefix*.")
        self.log("vanwatch.update[_cache](push=True)", "update cache.")

    def ingest(self):
        seed("abcli_aws_batch source - vanwatch/ingest - count=-1,publish")

    def list_layers(self):
        log('to update the cache run "vanwatch update_cache".', icon="🌱")
        return sorted(
            [
                os.path.splitext(os.path.basename(filename))[0]
                for filename in glob.glob(
                    os.path.join(
                        project.path,
                        "*.geojson",
                    )
                )
            ]
        )

    def load(
        self,
        prefix="",
        count=-1,
        refresh=True,
        timed=False,
    ) -> bool:
        list_layers = self.list_layers()
        if count != -1:
            list_layers = list_layers[-count:]

        for layer_name in list_layers:
            if not layer_name.startswith(prefix):
                continue

            filename = os.path.join(project.path, f"{layer_name}.geojson")

            QGIS.load(
                filename,
                layer_name,
                "template-timed" if timed else "template",
                refresh=False,
            )

        self.log(f"loaded {len(list_layers)} layer(s).")

        if refresh:
            QGIS.refresh()

    def unload(self, prefix="", refresh=True):
        log(prefix, icon="🗑️")

        for layer_name in [
            layer_name
            for layer_name in QGIS.list_of_layers()
            if layer_name.startswith(prefix)
        ]:
            QGIS.unload(layer_name, refresh=False)

        if refresh:
            QGIS.refresh()

    def update(self, push=False):
        self.update_cache(push)

    def update_cache(self, push=False):
        seed("vanwatch update_cache{}".format(" push" if push else ""))
