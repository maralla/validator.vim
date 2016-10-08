# -*- coding: utf-8 -*-

from validator import Validator


class ZshLint(Validator):
    __filetype__ = "zsh"

    checker = "zsh"
    args = "-n"
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            \s
            (?P<text>.*)"""
