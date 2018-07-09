#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Sergey Lyapustin',
    name="dcf",
    version="0.5.2",
    author_email="inoks@mail.ru",
    description="Django Classifieds Ads Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inoks/dcf",
    keywords='django classified ads',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
