from setuptools import setup

from blue_plugin import NAME, VERSION

setup(
    name=NAME,
    author="arash@kamangir.net",
    version=VERSION,
    description="template for an abcli plugin",
    packages=[NAME],
)
