from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nrc_adams_py",
    version="0.0.3",
    author="Brad Fox",
    author_email="bradfox2@gmail.com",
    description="Python Class connect to NRC ADAMS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bradfox2/nrc-adams-py",
    packages=find_packages(),
    test_suite = 'nose.collector',
    test_require = ['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
