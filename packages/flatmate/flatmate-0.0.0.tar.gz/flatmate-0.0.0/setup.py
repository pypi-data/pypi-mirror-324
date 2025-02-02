from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="flatmate",
    packages=["flatmate"],
    package_dir={"flatmate": "flatmate"},
    package_data={"flatmate": ["__init__.py"]},
    version="0.0.0",
    description="flatmate - Your Friendly Data Flattener. Converted Nested JSON from an API into a List of Single-Depth Dictionaries for Writing to a CSV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel J. Dufour",
    author_email="daniel.j.dufour@gmail.com",
    url="https://github.com/DanielJDufour/flatmate",
    download_url="https://github.com/DanielJDufour/flatmate/tarball/download",
    keywords=["csv", "data", "flat", "flatten"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["sendero"],
)
