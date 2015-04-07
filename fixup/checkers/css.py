# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Css(SyntaxChecker):
    __filetype__ = "css"
    __subname__ = "csslint"

    checker = "csslint"
    args = "--format=compact"
    regex = r"""
            .+:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (
               (?P<error>Error)
               |
               (?P<warning>Warning)
            )
            \s
            -
            \s
            (?P<text>.*)"""
