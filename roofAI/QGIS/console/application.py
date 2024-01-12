class ABCLI_QGIS_APPLICATION(object):
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        QGIS.log(self.name, "", icon=self.icon)

    def log(self, message, note=""):
        QGIS.log(message, note, icon=self.icon)
