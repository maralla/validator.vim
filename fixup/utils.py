# -*- coding: utf-8 -*-

from __future__ import absolute_import

import socket
import os
import os.path
import logging

log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "fixup.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logger = logging.getLogger("requests")
logger.propagate = False

g = {}


def get_unused_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


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
