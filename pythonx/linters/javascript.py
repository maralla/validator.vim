# -*- coding: utf-8 -*-

from linter import SyntaxChecker


class Javascript(SyntaxChecker):
    __filetype__ = "javascript"

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
