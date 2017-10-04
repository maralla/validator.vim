# -*- coding: utf-8 -*-

from validator import Validator


class GoFmtLint(Validator):
    __filetype__ = "go"

    default = True

    checker = "gofmt"
    args = "-l -e -d"
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (?P<text>.*)"""
