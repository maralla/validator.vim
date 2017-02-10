# -*- coding: utf-8 -*-

from validator import Validator


class LuacheckLint(Validator):
    __filetype__ = 'lua'

    checker = 'luacheck'
    args = '--no-color --codes'
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            \(
            (
                (?P<error>E\d+)
                |
                (?P<warning>W\d+)
            )
            \)
            \s
            (?P<text>.+)"""
