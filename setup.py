# -*- coding: utf-8 -*-
#
# Copyright 2019 Danny Lade.
#
"""
@author: Danny Lade
"""
from os import path
from setuptools import setup, find_packages


def __readme__():
    return open(path.join(path.dirname(__file__), 'README.md')).read()


setup(
    name='python-nullfs',
    version='0.8',
    author="Danny Lade",
    author_email="dannylade@gmail.com",
    description=("A client for the simple tron-like multi client online game called 'Traze' which is using MQTT for communication."),  # noqa
    license='GPLv3',
    keywords="fuse fusepy nullfs filesystem",
    url="https://github.com/DLade/python-nullfs",
    long_description=__readme__(),
    long_description_content_type='text/markdown',

    packages=find_packages('.'),

    install_requires=[
        'python_version>="3.5"',
        'fusepy==2.0.4',
    ],

    classifiers=[
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Filesystems",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
