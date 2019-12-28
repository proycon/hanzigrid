#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup

def read(fname):
    begin = False
    data = []
    with open(os.path.join(os.path.dirname(__file__), fname),'r',encoding='utf-8') as f:
        for line in f:
            if line.strip() == "Hanzi Grid Tool":
                begin = True
            if begin:
                data.append(line)
    return "".join(data)

setup(
    name = "hanzigrid",
    version = "0.1",
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("Generate a Chinese character grid for study"),
    license = "GPL",
    keywords = "chinese hanzi characters",
    url = "https://github.com/proycon/hanzigrid",
    packages=['hanzigrid'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    zip_safe=False,
    include_package_data=True,
    package_data = { 'hanzigrid': ['data/*.txt','input/*.txt'] },
    install_requires=[ 'svgwrite', 'pinyin-dec'],
    entry_points = {   'console_scripts': [ 'hanzigrid = hanzigrid.hanzigrid:main' ] }
)
