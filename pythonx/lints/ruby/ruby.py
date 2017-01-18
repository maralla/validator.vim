# -*- coding: utf-8 -*-

from validator import Validator


class Ruby(Validator):
    __filetype__ = "ruby"

    default = True

    checker = "ruby"
    args = "-c -w"
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            \s
            (?P<text>.*)"""

