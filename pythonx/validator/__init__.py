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

cache = collections.defaultdict(dict)


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
            Validator.registry[cls.__filetype__][cls.checker] = cls

        return super(Meta, cls).__init__(name, bases, attrs)

Base = Meta("Base", (object,), {})


class Unusable(object):
    def __get__(self, inst, owner):
        raise RuntimeError('unusable')


class Validator(Base):
    registry = collections.defaultdict(dict)

    __filetype__ = Unusable()
    checker = Unusable()

    default = False
    args = ''

    _regex_map = {}
    _cache = {}
    _type_map = None

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
                "type": _get_type(loc),
                "text": "[{}]{}".format(cls.checker, loc.get('text', ''))
            })
            lists.append(json.dumps(loc))
        return lists

    @classmethod
    def format_cmd(cls, fpath):
        if not cls.filter(fpath):
            return ''

        if not exe_exist(cls.checker):
            logging.warn("{} not exist".format(cls.checker))
            return ''

        if not os.path.exists(fpath):
            logging.warn("{} not exist".format(fpath))
            return ''

        return cls.cmd(fpath)

    @classmethod
    def _keygen(cls, file):
        return "{}-{}-{}".format(cls.__filetype__, cls.checker, file)

    @classmethod
    def parse_arguments(cls, file):
        key = cls._keygen(file)
        if key not in cls._cache:
            path = _find(file)
            cls._cache[key] = '' if path is None else _read_args(path)
        return cls._cache[key]

    @classmethod
    def filter(cls, fpath):
        return True

    @classmethod
    def cmd(cls, fname):
        return "{} {} {}".format(cls.checker, cls.args, fname)

_validator = Validator()


def load_checkers(ft, filters=None):
    if _validator._type_map is None:
        _validator._type_map = vim.eval('g:validator_filetype_map')

    ft = _validator._type_map.get(ft, ft)
    if ft not in _validator:
        try:
            importlib.import_module("lints.{}".format(ft))
        except ImportError:
            return {}
    checkers = _validator[ft]
    if not isinstance(filters, list):
        return {k: c for k, c in checkers.items() if c.default} or checkers

    return {k: c for k, c in checkers.items() if k in filters}
