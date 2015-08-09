# -*- coding: utf-8 -*-

from fixup import SyntaxChecker


class Css(SyntaxChecker):
    __filetype__ = "css"

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
