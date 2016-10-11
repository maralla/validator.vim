# -*- coding: utf-8 -*-

from validator import Validator


class EsLint(Validator):
    __filetype__ = "javascript"

    stdin = True
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

    def cmd(self, fname):
        args = "{} --stdin --stdin-filename {}".format(
            self.cmd_args, self.filename)
        return ' '.join([self.binary, args])
