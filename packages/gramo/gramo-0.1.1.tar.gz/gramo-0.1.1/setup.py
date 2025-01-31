from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

setup(
    name="gramo",
    version="0.1.1",
    packages=find_packages(),
    long_description=description,
    long_description_content_type="text/markdown",
    requires=[

    ]
)