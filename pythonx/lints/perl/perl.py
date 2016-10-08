# -*- coding: utf-8 -*-

from validator import Validator


class PerlLint(Validator):
    __filetype__ = "perl"

    checker = "perl"
    args = "-cw"
    regex = r"""
            (?P<text>.+?
            \sat\s.+?
            line\s
            (?P<lnum>\d+)
            \.$)"""
