from setuptools import find_packages, setup
import os
__version__ = "0.0.0"

setup(
    name='cliify',
    version=__version__,
    description='Package for creating a CLI from classes',
    packages=find_packages(),
    package_dir={
        "cliify": "cliify"
    },
    include_package_data=True,  # Ensures data files are included
    install_requires = [],
)
