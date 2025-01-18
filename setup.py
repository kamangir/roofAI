from roofAI import NAME, VERSION, DESCRIPTION
from blueness.pypi import setup


setup(
    filename=__file__,
    repo_name="roofAI",
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[
        NAME,
        f"{NAME}.dataset",
        f"{NAME}.dataset.ingest",
        f"{NAME}.help",
        f"{NAME}.semseg",
    ],
    include_package_data=True,
    package_data={
        NAME: [
            "config.env",
            "sample.env",
            ".abcli/**/*.sh",
        ],
    },
)
