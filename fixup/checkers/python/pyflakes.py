# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .. import SyntaxChecker


class PyFlakes(SyntaxChecker):
    __filetype__ = "python"
    __subname__ = "pyflakes"

    checker = "flake8"
    errorformat = ('%E%f:%l: could not compile,%-Z%p^,'
                   '%A%f:%l:%c: %t%n %m,'
                   '%A%f:%l: %t%n %m,'
                   '%-G%.%#')

    @classmethod
    def format_loclist(cls, loclist):
        for e in loclist:
            e["type"] = 'E' if e["type"] in 'EFC' else 'W'
