# -*- coding: utf-8 -*-

from validator import Validator


class CoffeeLint(Validator):
    __filetype__ = "coffee"

    stdin = True
    checker = "coffeelint"
    args = "--stdin --reporter csv"
    regex = r"""
            .+?,
            (?P<lnum>\d+),
            (?P<col>\d*),
            (
                (?P<error>error)
                |
                (?P<warning>warn)
            ),
            (?P<text>.*)"""
