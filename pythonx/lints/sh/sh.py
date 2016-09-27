# -*- coding: utf-8 -*-

from validator import Validator


class ShLint(Validator):
    __filetype__ = "sh"

    checker = "sh"
    args = "-n"
    regex = r"""
            .+?:\sline\s
            (?P<lnum>\d+):
            \s
            (?P<text>.*)"""
