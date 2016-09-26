# -*- coding: utf-8 -*-

from validator import Validator


class Sh(Validator):
    __filetype__ = "sh"

    checker = "shellcheck"
    args = "-x -f gcc"
    regex = r"""
            .+:
            (?P<lnum>\d+):
            (?P<col>\d+):
            .*
            \s
            (
               (?P<error>error)
               |
               (?P<warning>warning)
            ):
            \s
            (?P<text>.*)"""
