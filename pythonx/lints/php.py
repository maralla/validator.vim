# -*- coding: utf-8 -*-

from validator import Validator


class Php(Validator):
    __filetype__ = "php"

    checker = "php"
    args = "-l"
    regex = r"""
            .+:
            \s
            (?P<error>[\w\s]+),
            \s
            (?P<text>.*)
            \s
            in
            .*
            line\s(?P<lnum>\d+)"""
