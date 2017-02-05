# -*- coding: utf-8 -*-

from validator import Validator


class Jscs(Validator):
    __filetype__ = "javascript"

    checker = "jscs"
    args = "-r inline"
    regex = r"""
            .+?:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (?P<text>.+)"""
