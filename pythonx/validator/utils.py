# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import os.path
import platform
import vim

_dir = os.path.dirname(__file__)


def to_unicode(v):
    if isinstance(v, bytes):
        v = v.decode('utf-8')
    return v


def get_vim_var(name, default=None, unicode=False):
    v = vim.vars.get('validator_{}'.format(name), default)
    if unicode:
        v = to_unicode(v)
    return v


class _DebugFilter(object):
    def filter(self, record):
        return bool(get_vim_var('debug'))


def config_logging():
    logger = logging.getLogger('validator')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(os.path.dirname(_dir),
                                               'validator.log'))
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.addFilter(_DebugFilter())


def exe_exist(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        try_paths = []
        is_win = platform.system() == 'Windows'

        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            full_path = os.path.join(path, program)
            try_paths.append(full_path)
            if is_win:
                try_paths.append(full_path + '.exe')

        if any(map(is_exe, try_paths)):
            return True
    return False


def find_file(file):
    cwd = os.getcwd()
    while True:
        path = os.path.join(cwd, file)
        if os.path.exists(path):
            return path
        if cwd == '/':
            break
        cwd = os.path.split(cwd)[0]
