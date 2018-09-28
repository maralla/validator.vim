# -*- coding: utf-8 -*-

import os
from validator import Validator


class Gometalinter(Validator):
    __filetype__ = 'go'

    instant = False
    checker = 'gometalinter'
    args = '--fast'
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

    @property
    def cwd(self):
        return os.getcwd()

    def cmd(self, fpath):
        return ' '.join([self.binary, self.cmd_args, self.filename])
