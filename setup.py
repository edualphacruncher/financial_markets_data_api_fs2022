"""Python setup.py for _financial_markets_data_api_fs2022 package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("nvdata", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="financial_markets_data_api_fs2022",
    version=read("nvdata", "VERSION"),
    description="Financial Markets data API for Andrea Vedolin's course at MIT Sloan, Fall Semester 2022",
    url="https://github.com/edualphacruncher/financial_markets_data_api_fs2022",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="matek-alphacruncher",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    extras_require={"test": read_requirements("requirements-test.txt")},
)
