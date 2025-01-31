from setuptools import setup, find_packages

VERSION = '0.7.5'
DESCRIPTION = 'Python librarie for machine learning'
LONG_DESCRIPTION = 'Python librarie the provides useful tools for machine learning and data sience'


# Setting up
setup(
        name="scratchai", 
        version=VERSION,
        author="Mohamed Marghoub",
        author_email="<marghoubmohamed2@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'joblib'], # prerequisites

        keywords=['python', 'machine_learning', 'data_science'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)