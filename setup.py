#! /usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup

setup(name='buergen',
      author='ZNES',
      author_email='',
      description='',
      version='',
      url='https://github.com/znes/buergen',
      packages=find_packages(),
      license='',
      scripts=['bin/parser'],
      install_requires=[
        'docopt',
        'pandas',
        'requests',
        'django'],
      extras_require={}
      )
