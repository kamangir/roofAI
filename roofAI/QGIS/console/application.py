class ABCLI_QGIS_APPLICATION(object):
    def __init__(self, QGIS, name, icon):
        self.name = name
        self.icon = icon
        self.QGIS = QGIS

        QGIS.log(self.name, "", icon=self.icon)

    def log(self, message, note=""):
        self.QGIS.log(message, note, icon=self.icon)
