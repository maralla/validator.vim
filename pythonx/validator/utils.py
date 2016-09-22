# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import os.path
import platform
import vim

log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "validator.log")
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger("requests")
logger.propagate = False


class DebugFilter(object):
    def filter(self, record):
        return bool(int(vim.vars.get("validator_debug", 0)))

logging.root.addFilter(DebugFilter())


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
