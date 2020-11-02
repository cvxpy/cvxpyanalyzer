from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="cvxpyanalyzer",
    version="0.0.3",
    description="Analyzer for CVXPY problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["analyzer"],
    install_requires=["cvxpy >= 1.1.0a1", "requests", "setuptools"],
    license="Apache License, Version 2.0",
    url="https://github.com/cvxgrp/cvxpy-analyzer",
    classifiers=["Programming Language :: Python :: 3",],
)
