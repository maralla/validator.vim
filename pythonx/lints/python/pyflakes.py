# -*- coding: utf-8 -*-

from validator import Validator


class PyFlakes(Validator):
    __filetype__ = "python"

    checker = "flake8"
    args = "--filename=*"
    regex = r"""
            (.*?):
            (?P<lnum>\d+):
            (?P<col>\d+):
            \s
            (
                (?P<error>(E11|E9)\d+)
                |
                (?P<warning>(W|E|F4|F84|N*|C|D|Q|F)\d+)
            )
            \s
            (?P<text>.*)
            """
