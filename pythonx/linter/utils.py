# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import os.path
import logging

from .vim_utils import get_val

log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "linter.log")
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger("requests")
logger.propagate = False

g = {}


class DebugFilter(object):
    def filter(self, record):
        return bool(int(get_val("linter_debug")))

logging.root.addFilter(DebugFilter())


def exe_exist(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True
    return False
