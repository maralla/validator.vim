# -*- coding: utf-8 -*-

from __future__ import absolute_import

import collections
import importlib
import shlex
import subprocess
import os
import os.path
import re

from .utils import logging, exe_exist


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if name not in ("SyntaxChecker", "Base"):
            SyntaxChecker.registry[cls.__filetype__][cls.checker] = cls

        return super(Meta, cls).__init__(name, bases, attrs)

Base = Meta("Base", (object,), {})


class SyntaxChecker(Base):
    registry = collections.defaultdict(dict)

    errorformat = None
    checker = None
    args = ''

    _regex_map = {}

    def __getitem__(self, ft):
        return self.registry.get(ft, {})

    def __contains__(self, ft):
        return ft in self.registry

    @classmethod
    def parse_loclist(cls, loclist, bufnr):
        if cls.checker not in cls._regex_map:
            cls._regex_map[cls.checker] = re.compile(cls.regex, re.VERBOSE)

        lists = []
        for i, l in enumerate(loclist):
            g = cls._regex_map[cls.checker].match(l)
            if not g:
                continue

            loc = g.groupdict()
            loc.update({
                "enum": i + 1,
                "bufnr": bufnr,
                "valid": 1,
                "type": 'W' if loc["warning"] else 'E'
            })
            lists.append(loc)
        return lists

    @classmethod
    def gen_loclist(cls, fpath, bufnr):
        if not cls.filter_file(fpath):
            return []

        if not exe_exist(cls.checker):
            logging.warn("{} not exist".format(cls.checker))
            return []

        if not os.path.exists(fpath):
            logging.warn("{} not exist".format(fpath))
            return []

        cmd_args = shlex.split(cls.cmd(os.path.basename(fpath)))
        res = subprocess.Popen(cmd_args, cwd=os.path.dirname(fpath),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               close_fds=True)
        out = res.communicate()

        err_lines = '\n'.join(out).\
            strip().\
            replace('\r', '').\
            split('\n')

        loclists = cls.parse_loclist(err_lines, bufnr)
        return loclists

    @classmethod
    def filter_file(cls, fpath):
        return True

    @classmethod
    def cmd(cls, fname):
        return "{} {} {}".format(cls.checker, cls.args, fname)

checker_manager = SyntaxChecker()


def load_checkers(ft):
    if ft not in checker_manager:
        try:
            importlib.import_module("linters.{}".format(ft))
        except ImportError:
            return {}
    return checker_manager[ft]
