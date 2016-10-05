# -*- coding: utf-8 -*-

from validator import Validator


class Jshint(Validator):
    __filetype__ = "javascript"

    default = True

    checker = "jshint"
    args = "--verbose"
    regex = r"""
            .+?:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (?P<text>.+
            \s
            \(
                (
                    (?P<error>E)
                    |
                    (?P<warning>W)
                )
                (?P<code>\d+)
            \)
            )"""
