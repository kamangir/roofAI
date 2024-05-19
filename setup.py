from setuptools import setup
import os

from roofAI import NAME, VERSION, DESCRIPTION

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read().replace(
        "./",
        "https://github.com/kamangir/roofAI/raw/main/",
    )

setup(
    name=NAME,
    author="arash@kamangir.net",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[NAME],
)
