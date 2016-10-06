# -*- coding: utf-8 -*-

from validator import Validator


class LuacheckLint(Validator):
    __filetype__ = 'lua'

    checker = 'luacheck'
    args = '--no-color'
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (?P<text>.+)"""
