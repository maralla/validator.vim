# -*- coding: utf-8 -*-

from validator import Validator


class GolintLint(Validator):
    __filetype__ = "go"

    checker = 'golint'
    args = ''
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (?P<text>.*)"""
