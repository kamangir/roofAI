if not QGIS_is_live:
    from QGIS import QGIS
    from apps.vanwatch import ROOFAI_QGIS_APPLICATION_VANWATCH


vanwatch = ROOFAI_QGIS_APPLICATION_VANWATCH()
QGIS.add_application(vanwatch)

QGIS.intro()
