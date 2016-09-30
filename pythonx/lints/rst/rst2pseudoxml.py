# -*- coding: utf-8 -*-

from validator import Validator


class RST2PseudoXMLLint(Validator):
    __filetype__ = "rst"

    checker = "rst2pseudoxml.py"
    args = "--report=2"
    regex = r"""
            .+?:
            (?P<lnum>\d+)?:
            \s\(
            (
                (?P<error>(ERROR|SEVERE)/\d)
                |
                (?P<warning>(WARNING)/\d)
            )
            \)\s
            (?P<text>.+[.:])"""
