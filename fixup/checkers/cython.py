# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Cython(SyntaxChecker):
    __filetype__ = "cython"
    __subname__ = "cython"

    checker = "cython"
    args = "--warning-extra"
    errorformat = ('%Wwarning: %f:%l:%c: %m,'
                   '%E%f:%l:%c: %m')

    @classmethod
    def filter_file(cls, fname):
        if fname.endswith(".pxd"):
            return False
        return True
