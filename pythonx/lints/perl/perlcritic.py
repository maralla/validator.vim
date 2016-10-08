# -*- coding: utf-8 -*-

from validator import Validator


class PerlCriticLint(Validator):
    __filetype__ = "perl"

    checker = "perlcritic"
    args = "--gentle --quiet --nocolor"
    regex = r"""
            (?P<text>.+?
            \sat\sline\s
            (?P<lnum>\d+),
            \scolumn\s
            (?P<col>\d+)\.
            .+?
            \(Severity:\s
            (?P<code>\d+)
            \)
            )"""
