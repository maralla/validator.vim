# -*- coding: utf-8 -*-

from validator import Validator


class EsLint(Validator):
    __filetype__ = "javascript"

    checker = "eslint"
    args = "-f compact --no-color"
    args_file = ".eslint-config"
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

    @classmethod
    def cmd(cls, fname):
        return "{} {} {} {}".format(cls.checker, cls.args,
                                    cls.parse_arguments(cls.args_file), fname)
