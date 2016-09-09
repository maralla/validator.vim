# -*- coding: utf-8 -*-

from validator import Validator


class EsLint(Validator):
    __filetype__ = "javascript"

    checker = "eslint"
    args = "-f compact --no-color"
    regex = r"""
            .+?:
            \sline\s(?P<lnum>\d+),
            \scol\s(?P<col>\d+),
            \s
            (
                (?P<error>Error)
                |
                (?P<warning>Warning)
            )
            \s-\s
            (?P<text>.*)"""
