# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Cython(SyntaxChecker):
    __filetype__ = "cython"
    __subname__ = "cython"

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

    @classmethod
    def filter_file(cls, fname):
        if fname.endswith(".pxd"):
            return False
        return True
