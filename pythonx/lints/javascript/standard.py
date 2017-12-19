# -*- coding: utf-8 -*-

from validator import Validator


class Standard(Validator):
    __filetype__ = 'javascript'

    stdin = True
    checker = 'standard'
    args = '--stdin'
    regex = r"""
        .+?:
        (?P<lnum>\d+):
        (?P<col>\d+):
        \s
        (?P<text>.*)
    """
