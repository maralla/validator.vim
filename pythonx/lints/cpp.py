# -*- coding: utf-8 -*-

from validator import Validator


class Cpp(Validator):
    __filetype__ = "cpp"

    checker = "clang-tidy"
    args_file = ".clang-tidy-config"
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

    @classmethod
    def cmd(cls, fname):
        return "{} {} -- {}".format(
            cls.checker, fname, cls.parse_arguments(cls.args_file))
