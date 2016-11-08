#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Christian Karrié <christian@karrie.info>'

from distutils.core import setup

# Dynamically calculate the version based on ccm.VERSION
version_tuple = __import__('tvh').VERSION
version = ".".join([str(v) for v in version_tuple])

setup(
    name='python-htspclient',
    description='TVHeadend HTSP Client Library',
    version=version,
    author='Christian Karrie',
    author_email='ckarrie@gmail.com',
    url='https://bitbucket.org/ckarrie/python-htspclient',
    packages=['tvh'],
)
