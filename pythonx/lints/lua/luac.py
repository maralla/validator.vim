# -*- coding: utf-8 -*-

from validator import Validator


class LuaCLint(Validator):
    __filetype__ = 'lua'

    checker = 'luac'
    args = '-p'
    regex = r"""
            luac:\s.+?:
            (?P<lnum>\d+):\s
            (?P<text>.+)"""
