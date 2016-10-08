# -*- coding: utf-8 -*-

from validator import Validator


class EsLint(Validator):
    __filetype__ = "javascript"

    stdin = True
    checker = "eslint"
    args = "-f compact --no-color --stdin"
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
        args = "{} --stdin-filename {}".format(cls.args, cls.filename())
        return ' '.join([cls.checker, args])
