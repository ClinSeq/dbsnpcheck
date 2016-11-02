#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Based on https://github.com/pypa/sampleproject/blob/master/setup.py."""

from __future__ import unicode_literals
from setuptools import setup, find_packages
# To use a consistent encoding
import codecs


def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))

        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires


setup(name='dbsnpcheck',
      author='Daniel Klevebring',
      author_email='daniel.klevebring@gmail.com',
      url='https://github.com/clinseq/dbsnpcheck',
      description='Count how many somatic SNVs are present in dbSNP',
      version='0.0.1',
      download_url='https://github.com/clinseq/dbsnpcheck/tarball/v0.0.1',
      packages=find_packages(exclude=('tests*', 'docs', 'examples')),
      keywords=['testing', 'genomics'],
      install_requires=parse_reqs(),
      entry_points={'console_scripts': [
          'dbsnpcheck = dbsnpcheck.cli:base'
      ]}
      )
