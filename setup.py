from roofAI import NAME, VERSION, DESCRIPTION
from blueness.pypi import setup


setup(
    filename=__file__,
    repo_name="roofAI",
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[NAME],
    include_package_data=True,
    package_data={
        NAME: [
            ".abcli/**/*.sh",
        ],
    },
)
