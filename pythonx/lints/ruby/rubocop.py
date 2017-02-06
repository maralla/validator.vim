# -*- coding: utf-8 -*-

from validator import Validator


class Rubocop(Validator):
    __filetype__ = 'ruby'

    checker = 'rubocop'
    args = '-f s -c .rubocop.yml'
    regex = r"""
            (
                (?P<error>E)
                |
                (?P<warning>(W|C))
            ):
            \s*
            (?P<lnum>\d+):
            \s*
            (?P<col>\d+):
            \s*
            (?P<text>.*)
            """
