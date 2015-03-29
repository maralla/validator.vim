# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .. import SyntaxChecker


class PyFlakes(SyntaxChecker):
    __filetype__ = "python"
    __subname__ = "pyflakes"

    checker = "flake8"
    regex = r"""
            (.*?):
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (
                (?P<error>(E11|E9)\d+)
                |
                (?P<warning>(W|E|F4|F84|N*|C|D|Q|F)\d+)
            )
            \s
            (?P<text>.*)
            """

    @classmethod
    def format_loclist(cls, loclist):
        for e in loclist:
            e["type"] = 'E' if e["type"] in 'EFC' else 'W'
