# -*- coding: utf-8 -*-

from validator import Validator


class Gometalinter(Validator):
    __filetype__ = 'go'

    checker = 'gometalinter'
    # <file>:<line>:[<column>]: <message> (<linter>)
    regex = r"""
        .+?:
        (?P<lnum>\d+):
        (?P<col>\d+)?:
        (
            (?P<error>error)
            |
            (?P<warning>.*?)
        ):
        \s
        (?P<text>.*)
    """
