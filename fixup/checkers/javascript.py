# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Javascript(SyntaxChecker):
    __filetype__ = "javascript"
    __subname__ = "jshint"

    checker = "jshint"
    args = "--verbose"
    errorformat = "%A%f: line %l\, col %v\, %m \(%t%n\)"
