# -*- coding: utf-8 -*-

from validator import Validator


class Css(Validator):
    __filetype__ = 'css'

    checker = 'csslint'
    args = '--format=compact'
    regex = r'''
            .+:
            \s
            line\s(?P<lnum>\d+),
            \s
            col\s(?P<col>\d+),
            \s
            (
               (?P<error>Error)
               |
               (?P<warning>Warning)
            )
            \s
            -
            \s
            (?P<text>.*)'''
