#!/usr/bin/env python3
#  -*- encoding: utf-8 -*-

__author__ = "Adler Neves"
__email__ = "adlerosn@gmail.com"
__title__ = None
__description__ = None
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Adler O. S. Neves'
__version__ = '0.0.1'

class Objectify(object):
    def __init__(self, d: dict):
        self.__dict__ = d
    @property
    def as_dict(self):
        return self.__dict__
