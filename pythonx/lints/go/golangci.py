# -*- coding: utf-8 -*-

import logging
import os
import re
import json
from validator import Validator, get_type

logger = logging.getLogger('validator')

# ERRO Running error: buildssa: analysis skipped: errors in package: [/home/maralla/Workspace/projects/zest/auth/auth.go:25:37: undeclared name: tokenRpc]

class Golangci(Validator):
    __filetype__ = 'go'

    instant = False
    checker = 'golangci-lint'
    args = '--out-format line-number'
    regex = re.compile(r"""
        (?P<fname>.+?):
        (?P<lnum>\d+):
        ((?P<col>\d+):)?
        \s
        (?P<text>.*)
    """, re.VERBOSE)

    @property
    def cwd(self):
        return os.getcwd()

    def parse_loclist(self, loclist, bufnr):
        fname = os.path.basename(self.filename)

        lists = []
        for i, l in enumerate(loclist):
            logger.info("%r", l)
            g = self.regex.match(l)
            if not g:
                continue

            loc = g.groupdict()
            if os.path.basename(loc.get('fname', '')) != fname:
                continue
            col = loc.get('col', -1)
            loc.update(self.compose_loc(i + 1, bufnr, get_type(loc),
                                        loc.get('text', ''), col))
            lists.append(loc)

        return json.dumps(lists)

    def cmd(self, fpath):
        package = os.path.dirname(self.filename)
        logger.info(package)
        return ' '.join([self.binary, "run", self.cmd_args, package])
