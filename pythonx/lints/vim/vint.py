# -*- coding: utf-8 -*-

from validator import Validator


class VimVint(Validator):
    __filetype__ = 'vim'

    checker = 'vint'
    args = '-w --no-color'
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s(?P<text>.+)"""
