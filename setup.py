"""Setuptools Module."""
from setuptools import setup, find_packages

setup(
    name="singleton",
    version="0.1",
    packages=find_packages(),
    extras_require={
        'dev': ['pylint',
                'pycodestyle',
                'pydocstyle',
                'pytest',
                'coverage',
                'pytest-cov'],
    },
    # metadata for upload to PyPI
    author="Alexander Richards",
    author_email="a.richards@imperial.ac.uk",
    description="Singleton base class and decorator",
    license="MIT",
    keywords="singleton",
    url="https://github.com/alexanderrichards/Singleton"
)
