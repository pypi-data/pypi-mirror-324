from setuptools import setup, find_namespace_packages
from pathlib import Path


version = "0.0.5"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="outerbounds_app_client",
    version=version,
    description="Experimental client for interacting with Outerbounds apps programmatically",
    author="Outerbounds, Inc.",
    license="Commercial",
    packages=find_namespace_packages(include=["outerbounds_app_client"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "boto3",
        "requests",
    ],
)
