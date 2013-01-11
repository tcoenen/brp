#!/usr/bin/env python
from distutils.core import setup

setup(
    name='Browser Plot',
    version='0.1-dev',
    packages=['brp', 'brp.core', 'brp.svg', 'brp.svg.plotters'],
    license='',
    long_description=open('README.md').read(),
)
