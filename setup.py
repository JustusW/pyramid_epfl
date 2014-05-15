#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2014 solute GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

from setuptools import setup

setup(
    name='EPFL Python Frontend Logic',
    version='0.1.0',
    author='Gunter Bach',
    author_email='gb@solute.de',
    packages=['solute.epfl', 'solute.epfl.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/epfl/',
    license='LICENSE.txt',
    description='The EPFL Python Frontend Logic.',
    long_description=open('README.md').read(),
    install_requires=[
        "pyramid >= 1.4",
        "Jinja2 >= 2.7.2",
        "WTForms >= 1.0.5",
        "pyramid_jinja2 >= 1.10",
        "ujson >= 1.33",
    ],
    entry_points = """\
    [pyramid.scaffold]
    pyramid_epfl_starter=solute.epfl.scaffolds:EPFLStarterTemplate
    pyramid_epfl_notes=solute.epfl.scaffolds:EPFLNotesTemplate
    """
)

