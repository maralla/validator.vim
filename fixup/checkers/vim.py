# -*- coding: utf-8 -*-

from __future__ import absolute_import

import vim

from . import SyntaxChecker


class Vim(SyntaxChecker):
    __filetype__ = "vim"
    __subname__ = "vim"

    checker = "vim"
    args = ("-esnN -V1 -i NONE \"+set rtp={rtp}\""
            " -S {filename} \"+echo '\\r'\" +quit")
    errorformat = ("%+PError detected while processing %f:%.%#,"
                   "%Aline\ %#%l:%.%#,%Z%t%n: %m,"
                   "%-Gnot found%.%#,"
                   "%-GE%n:%.%#,"
                   "%-QError detected while processing function%.%#,"
                   "%-Q")

    @classmethod
    def cmd(cls, fname):
        rtp = vim.eval("&rtp")
        args = cls.args.format(rtp=rtp, filename=fname)
        return "{} {}".format(cls.checker, args)
