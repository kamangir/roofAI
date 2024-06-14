if not QGIS_is_live:
    from application import ROOFAI_QGIS_APPLICATION
    from project import project


class ROOFAI_QGIS_APPLICATION_UKRAINE_TIMEMAP(ROOFAI_QGIS_APPLICATION):
    def __init__(self):
        super().__init__("ukraine_timemap", "🇺🇦")

    def help(self):
        self.log(
            'ukraine_timemap.update("dryrun,~upload")',
            f"update {project.name}.",
        )

    def update(self, options: str = ""):
        self.log(f"ukraine_timemap.update({options}): {project.name}")

        self.log("🪄")

