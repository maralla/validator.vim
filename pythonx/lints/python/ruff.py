# -*- coding: utf-8 -*-

import re
import json
from validator import Validator


class Ruff(Validator):
    __filetype__ = "python"

    checker = "ruff"
    args = "check --output-format json-lines"

    def parse_loclist(self, loclist, bufnr):
        lists = []

        for i, l in enumerate(loclist):
            try:
                data = json.loads(l)
            except Exception:
                continue

            loc = self.compose_loc(
                i + 1, bufnr, 'W',
                '({}) {}'.format(data['code'], data['message']),
                data['location']['column']
            )

            loc['lnum'] = data['location']['row']
            lists.append(loc)

        return json.dumps(lists)
