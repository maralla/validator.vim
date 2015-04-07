#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
import importlib
import os
import os.path
import sys
import signal

path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)

from fixup.checkers import SyntaxChecker
from fixup.transport import ServerHandler, make_server
from fixup.utils import logging

checker_manager = SyntaxChecker()


class FuHandler(ServerHandler):
    def check(self, req):
        ft = req["ft"]
        if ft not in checker_manager:
            try:
                importlib.import_module("fixup.checkers.{}".format(ft))
            except ImportError as e:
                logging.exception(e)
                return {}

        checker_classes = checker_manager[ft]

        errors = {}
        for checker_name, checker in checker_classes.items():
            errors[checker_name] = checker.gen_loclist(
                req["fpath"], req["bufnr"])

        logging.info("check {}".format(errors))

        return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    args = parser.parse_args()

    try:
        os.setsid()
    except OSError:
        pass

    sys.stdin.close()
    os.close(0)

    def sig_handler(signum, frame):
        sys.exit()

    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, sig_handler)

    server = make_server(args.port, FuHandler)
    logging.info("serve at localhost:{}".format(args.port))
    server.serve_forever()


if __name__ == "__main__":
    main()
