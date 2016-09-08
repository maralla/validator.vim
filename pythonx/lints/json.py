# -*- coding: utf-8 -*-

from validator import Validator


class Json(Validator):
    __filetype__ = "json"

    checker = "jsonlint"
    args = "-q -c"
    regex = r"""
            .+?:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (?P<text>.+)"""
