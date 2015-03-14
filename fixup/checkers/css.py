#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Css(SyntaxChecker):
    __filetype__ = "css"
    __subname__ = "csslint"

    checker = "csslint"
    args = "--format=compact"
    errorformat = ("%-G,"
                   "%-G%f: lint free!,"
                   "%f: line %l\, col %c\, %trror - %m,"
                   "%f: line %l\, col %c\, %tarning - %m,"
                   "%f: line %l\, col %c\, %m")
