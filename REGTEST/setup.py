from setuptools import setup, find_packages

setup(
    name="samuel_regression_lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.0.0",
    ],
)