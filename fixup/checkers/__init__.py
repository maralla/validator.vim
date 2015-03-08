# -*- coding: utf-8 -*-

from __future__ import absolute_import

import collections
import subprocess
import os.path


def safe_str(lst):
    r = []
    for e in lst:
        r.append('"{}"'.format(e.replace('"', '\\"')))
    return '[{}]'.format(','.join(r))


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if name not in ("SyntaxChecker", "Base"):
            SyntaxChecker.registry[cls.__filetype__][
                cls.__subname__] = cls

        return super(Meta, cls).__init__(name, bases, attrs)

Base = Meta('Base', (object,), {})


class SyntaxChecker(Base):
    registry = collections.defaultdict(dict)

    errorformat = None
    checker = None
    args = ''

    def __getitem__(self, ft):
        return self.registry.get(ft, {})

    def __contains__(self, ft):
        return ft in self.registry

    @classmethod
    def get_loclist(cls):
        import vim

        if cls.checker is None:
            raise Exception("No checker")

        fpath = vim.eval("expand('%:p')")
        fdir = os.path.dirname(fpath)

        r = cls.filter_file(fpath)
        if not r:
            return []

        res = subprocess.Popen(cls.cmd(fpath), shell=True, cwd=fdir,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = res.communicate()
        out = '\n'.join(out)
        err_lines = out.strip().replace('\r', '').split('\n')

        if cls.errorformat:
            vim.command("let old_fmt = &errorformat")
            vim.command("let &errorformat = '{}'".format(cls.errorformat))

        vim.command("let expr_str = {}".format(safe_str(err_lines)))
        vim.command("lgetexpr expr_str")
        vim.command("unlet expr_str")
        errors = vim.eval("getloclist(0)")

        if cls.errorformat:
            vim.command("let &errorformat = old_fmt")
            vim.command("unlet old_fmt")

        loclist = []
        for i, e in enumerate(errors):
            if e["valid"] == '0' or e['bufnr'] == '0':
                continue
            e["nr"] = i + 1
            e["text"] = e["text"].strip()
            loclist.append(e)
        cls.format_loclist(loclist)

        return loclist

    @classmethod
    def format_loclist(cls, loclist):
        pass

    @classmethod
    def filter_file(cls, fname):
        return True

    @classmethod
    def cmd(cls, fname):
        return "{} {} {}".format(cls.checker, cls.args, fname)
