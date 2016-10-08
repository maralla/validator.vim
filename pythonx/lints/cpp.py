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

    def cmd(self, fname):
        return "{} {} -- {}".format(
            self.exe, fname, self.parse_arguments(self.args_file))
