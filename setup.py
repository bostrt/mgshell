#!/usr/bin/env python3
from setuptools import setup, find_packages
from mgshell.version import __version__

# NOTE: Update the __version__ flag in mgshell/version.py for release.

setup(
    name='mgshell',
    version=__version__,
    packages=find_packages(),
    author='bostrt',
    entry_points = {
        'console_scripts': [
            'mg=mgshell.mgshell:cli',
            'ns=mgshell.ns:ns',
            'pod=mgshell.pod:pod',
            'log=mgshell.log:log',
            'root=mgshell.root:root',
            ]
    },
    description='xxx',
    license='',
    url='https://github.com/bostrt/mgshell',
    install_requires=[
        'click', 
        'fuzzyfinder'
        ]
)
