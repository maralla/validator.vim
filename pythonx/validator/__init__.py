# -*- coding: utf-8 -*-

from __future__ import absolute_import

import collections
import importlib
import json
import re
import vim
import logging

from .utils import config_logging, exe_exist, get_vim_var, to_unicode, \
    find_file


config_logging()
logger = logging.getLogger('validator')


def _get_type(msg):
    if msg.get('error') is not None:
        return 'E'
    if msg.get('warning') is not None:
        return 'W'

    return 'E' if msg.get('type', 'error').lower() == 'error' else 'W'


def _read_args(path):
    try:
        with open(path) as f:
            return ' '.join((l.strip() for l in f.readlines()))
    except Exception:
        return ''


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('Validator', 'Base'):
            Validator._registry[cls.__filetype__][cls.checker] = cls()

        return super(Meta, cls).__init__(name, bases, attrs)


Base = Meta('Base', (object,), {})


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

    # Option name for user to specify checker arguments
    args_option = None
    # binary name for user to specify the path of the checker executable
    binary_option = None

    # Check when text changed.
    instant = True

    _regex_map = {}
    _cache = {}
    _type_map = {
        b'c': b'cpp'
    }

    def __getitem__(self, ft):
        return self._registry.get(ft, {})

    def __contains__(self, ft):
        return ft in self._registry

    def compose_loc(self, enum, bufnr, buf_type, text):
        return {
            'enum': enum,
            'bufnr': bufnr,
            'type': buf_type,
            'text': '[{}]{}'.format(self.checker, text)
        }

    def parse_loclist(self, loclist, bufnr):
        logger.info('parse input = %s', [self, loclist, bufnr])

        if self.checker not in self._regex_map:
            self._regex_map[self.checker] = re.compile(self.regex, re.VERBOSE)

        lists = []
        for i, l in enumerate(loclist):
            g = self._regex_map[self.checker].match(l)
            if not g:
                continue

            loc = g.groupdict()
            loc.update(self.compose_loc(i + 1, bufnr, _get_type(loc),
                                        loc.get('text', '')))
            lists.append(loc)

        logger.info('parsed lists = %s', lists)
        return json.dumps(lists)

    def format_cmd(self, fpath):
        if not self.filter(fpath):
            return ''

        if not exe_exist(self.binary):
            logger.warning('%s not exist', self.binary)
            return ''

        return self.cmd(fpath)

    @property
    def cwd(self):
        pass

    def parse_arguments(self, file):
        key = '{}-{}-{}'.format(self.__filetype__, self.checker, file)
        if key not in self._cache:
            path = find_file(file)
            self._cache[key] = '' if path is None else _read_args(path)
        return self._cache[key]

    def filter(self, fpath):
        return True

    @property
    def filename(self):
        return vim.current.buffer.name

    @property
    def binary(self):
        name = self.binary_option or '{}_{}'.format(
            self.__filetype__, self.checker)

        v = get_vim_var('{}_binary'.format(name), b'', unicode=True)
        return v or self.checker

    @property
    def cmd_args(self):
        name = self.args_option or '{}_{}'.format(
            self.__filetype__, self.checker)

        v = get_vim_var('{}_args'.format(name), b'', unicode=True)
        return v or self.args

    @property
    def type_map(self):
        v = get_vim_var('filetype_map', {})
        self._type_map.update(v)
        return self._type_map

    def cmd(self, fname):
        return "{} {} {}".format(self.binary, self.cmd_args, fname)


_validator = Validator()


def _get_filters(ft):
    """
    :param ft: unicode
    """
    checkers = get_vim_var('{}_checkers'.format(ft))
    filters = None
    if isinstance(checkers, (list, vim.List)):
        filters = []
        for c in checkers:
            try:
                c = to_unicode(c)
            except Exception as e:
                logger.exception(e)
                continue
            filters.append(c)
    else:
        try:
            filters = [to_unicode(checkers)]
        except Exception as e:
            logger.exception(e)
    return filters


def load_checkers(ft):
    """
    :param ft: bytes
    """
    if not ft:
        return {}

    ft = to_unicode(_validator.type_map.get(ft, ft))
    if ft not in _validator:
        try:
            importlib.import_module('lints.{}'.format(ft))
        except ImportError:
            try:
                importlib.import_module('validator_{}'.format(ft))
            except ImportError:
                _validator._registry[ft] = {}
    checkers = _validator[ft]

    if not checkers:
        return {}

    filters = _get_filters(ft)
    if filters is None:
        return {k: c for k, c in checkers.items() if c.default} or checkers

    return {k: c for k, c in checkers.items() if k in filters}
