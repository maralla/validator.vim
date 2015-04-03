# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import SyntaxChecker


class Javascript(SyntaxChecker):
    __filetype__ = "javascript"
    __subname__ = "jshint"

    checker = "jshint"
    args = "--verbose"
    regex = r"""
            .+?:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (?P<text>.+)
            \s
            \(
                (
                    (?P<error>E)
                    |
                    (?P<warning>W)
                )
                (?P<code>\d+)
            \)"""
