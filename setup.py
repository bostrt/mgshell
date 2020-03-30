#!/usr/bin/env python3
from setuptools import setup, find_packages
from mgshell.version import __version__

# NOTE: Update the __version__ flag in mgshell/version.py for release.

setup(
    name='mgshell',
    author='Robert Bost',
    author_email='bostrt at gmail dot com',
    description='A command line aid for navigating OpenShift 4 must gather reports.',
    license='MIT',
    url='https://github.com/bostrt/mgshell',
    keywords='must-gather openshift tools techsupport',
    version=__version__,
    packages=find_packages(),
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': [
            'mg=mgshell.mgshell:cli',
            'ns=mgshell.ns:ns',
            'pod=mgshell.pod:pod',
            'log=mgshell.log:log',
            'root=mgshell.root:root',
            ]
    },
    install_requires=[
        'click', 
        'fuzzyfinder'
        ]
)
