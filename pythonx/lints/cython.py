# -*- coding: utf-8 -*-

from validator import Validator


class Cython(Validator):
    __filetype__ = "cython"

    checker = "cython"
    args = "--warning-extra"
    regex = r"""
            (?P<warning>warning)?
            (.*?):
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (?P<text>.*)
            """

    def filter(self, fname):
        if fname.endswith(".pxd"):
            return False
        return True
