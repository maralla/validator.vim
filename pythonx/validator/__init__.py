# -*- coding: utf-8 -*-

from __future__ import absolute_import

import collections
import importlib
import json
import os
import os.path
import re
import vim

from .utils import logging, exe_exist


def _get_type(msg):
    if msg.get('error') is not None:
        return 'E'
    if msg.get('warning') is not None:
        return 'W'

    return 'E' if msg.get('type', 'error').lower() == 'error' else 'W'


def _find(file):
    cwd = os.getcwd()
    while True:
        path = os.path.join(cwd, file)
        if os.path.exists(path):
            return path
        if cwd == '/':
            break
        cwd = os.path.split(cwd)[0]


def _read_args(path):
    try:
        with open(path) as f:
            return ' '.join((l.strip() for l in f.readlines()))
    except Exception:
        return ''


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if name not in ("Validator", "Base"):
            Validator._registry[cls.__filetype__][cls.checker] = cls()

        return super(Meta, cls).__init__(name, bases, attrs)

Base = Meta("Base", (object,), {})


class Unusable(object):
    def __get__(self, inst, owner):
        raise RuntimeError('unusable')


class Validator(Base):
    """ Base class for all checkers

    Subclass must provide both `__filetype__` and `checker` attributes.
    """
    _registry = collections.defaultdict(dict)

    # File type the checker works on.
    __filetype__ = Unusable()
    # Checker name
    checker = Unusable()

    # When `True` the checker read file content from stdin. `False` means the
    # checker read file content from a temporary file.
    stdin = False
    # If a file type has default checkers, only the defaults are used for
    # checking. If no defaults, all checkers are used. If the user defined
    # `g:validator_<filetype>_checkers`, the defined checkers has the highest
    # priority and are used for checking.
    default = False
    # Arguments for the checker.
    args = ''

    _regex_map = {}
    _cache = {}
    _type_map = {
        'c': 'cpp'
    }

    def __getitem__(self, ft):
        return self._registry.get(ft, {})

    def __contains__(self, ft):
        return ft in self._registry

    def parse_loclist(self, loclist, bufnr):
        if self.checker not in self._regex_map:
            self._regex_map[self.checker] = re.compile(self.regex, re.VERBOSE)

        lists = []
        for i, l in enumerate(loclist):
            g = self._regex_map[self.checker].match(l)
            if not g:
                continue

            loc = g.groupdict()
            loc.update({
                "enum": i + 1,
                "bufnr": bufnr,
                "type": _get_type(loc),
                "text": "[{}]{}".format(self.checker, loc.get('text', ''))
            })
            lists.append(loc)
        return json.dumps(lists)

    def format_cmd(self, fpath):
        if not self.filter(fpath):
            return ''

        if not exe_exist(self.exe):
            logging.warn("{} not exist".format(self.exe))
            return ''

        return self.cmd(fpath)

    def parse_arguments(self, file):
        key = '{}-{}-{}'.format(self.__filetype__, self.checker, file)
        if key not in self._cache:
            path = _find(file)
            self._cache[key] = '' if path is None else _read_args(path)
        return self._cache[key]

    def filter(self, fpath):
        return True

    @property
    def filename(self):
        return vim.current.buffer.name

    @property
    def exe(self):
        return vim.eval('validator#utils#option("exe", "{}", "{}")'.format(
            self.__filetype__, self.checker)) or self.checker

    @property
    def cmd_args(self):
        return vim.eval('validator#utils#option("args", "{}", "{}")'.format(
            self.__filetype__, self.checker)) or self.args

    @property
    def type_map(self):
        m = vim.eval('get(g:, "validator_filetype_map", {})')
        self._type_map.update(m)
        return self._type_map

    def cmd(self, fname):
        return "{} {} {}".format(self.exe, self.cmd_args, fname)

_validator = Validator()


def load_checkers(ft):
    if not ft:
        return {}

    ft = _validator.type_map.get(ft, ft)
    filters = vim.eval('get(g:, "validator_{}_checkers")'.format(ft))

    if ft not in _validator:
        try:
            importlib.import_module("lints.{}".format(ft))
        except Exception as e:
            logging.exception(e)
            _validator._registry[ft] = {}
    checkers = _validator[ft]

    if not checkers:
        return checkers

    if not isinstance(filters, list):
        return {k: c for k, c in checkers.items() if c.default} or checkers

    return {k: c for k, c in checkers.items() if k in filters}
