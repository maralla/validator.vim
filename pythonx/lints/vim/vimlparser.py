# -*- coding: utf-8 -*-

from validator import Validator


class VimLParserLint(Validator):
    __filetype__ = 'vim'

    checker = 'vimlparser'
    args = ''
    regex = r"""
            .+?:
            (?P<lnum>\d+):
            (?P<col>\d+):
            \svimlparser:\s
            (?P<text>
                (
                    (
                        (?P<error>E)
                        |
                        (?P<warning>W)
                    )
                    (?P<code>\d+):\s
                )?
                .+
            )"""
