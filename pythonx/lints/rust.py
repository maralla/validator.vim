#! /usr/bin/env python

from __future__ import absolute_import

import json
import re
import os
import logging
from validator import Validator
from validator.utils import find_file


PAT = re.compile('\s+-->\s(?P<fname>.*?):(?P<lnum>\d+):(?P<col>\d+)')

logger = logging.getLogger('validator')


class Cargo(Validator):
    __filetype__ = 'rust'

    instant = False
    checker = 'cargo'
    args = 'check --color never'

    def parse_loclist(self, loclist, bufnr):
        logger.info('parse input = %s', [self, loclist, bufnr])
        lists = []
        j = 0
        cwd = self.cwd
        for i, l in enumerate(loclist):
            r = PAT.match(l)
            if r:
                j += 1
                msg = r.groupdict()
                fname = msg.get('fname')
                if not fname:
                    continue
                path = os.path.join(cwd, fname)
                if path != self.filename:
                    continue
                text = loclist[i - 1] if i > 0 else ''
                ty = 'E' if text.startswith('error') else 'W'
                loc = self.compose_loc(j, bufnr, ty, text)
                loc.update(msg)
                lists.append(loc)
        logger.info(lists)
        return json.dumps(lists)

    def cmd(self, fname):
        return '{} {}'.format(self.binary, self.args)

    @property
    def cwd(self):
        return os.path.dirname(find_file('Cargo.toml'))
