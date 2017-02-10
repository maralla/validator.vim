# -*- coding: utf-8 -*-

from validator import Validator
import os.path


class GoMetalinterLint(Validator):
    __filetype__ = "go"

    checker = 'gometalinter'
    args = '--enable-all'
    regex = r"""
            .+?:
            (?P<lnum>\d+)?:
            (?P<col>\d+)?:
            (
                (?P<warning>(warning))
                |
                (?P<error>(error))
            )
            :\s
            (?P<text>.*)"""

    def cmd(self, fname):
        return "{} {} {}".format(
                self.checker, self.args, os.path.dirname(os.path.abspath(fname)))
