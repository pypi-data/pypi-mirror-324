from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    description = fh.read()
try:
    originalFile = './dbiu_databases/wetterdaten.db'  # modify this line to choose a database file
    dbFile = './dbiu_databases/base.db'
    bakFile = dbFile+'.bak'

    if os.path.isfile(dbFile):
        os.rename(dbFile, bakFile)
    os.rename(originalFile, dbFile)



    setup(
        name='dbiu_databases',
        version='18',  # modify this line to set a package version, one version for each DB
        packages=find_packages(),
        install_requires=[
        ],
        long_description=description,
        long_description_content_type="text/markdown",
        package_data={
            'dbiu_databases': [
                'base.db'
                ]
        },
        include_package_data=True
    )

finally:
    if os.path.isfile(dbFile):
        os.rename(dbFile,originalFile)
    if os.path.isfile(bakFile):
        os.rename(bakFile,dbFile)
