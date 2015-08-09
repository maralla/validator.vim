# -*- coding: utf-8 -*-

from __future__ import print_function

import collections
import uuid

from .vim_utils import place_sign, unplace_sign


class _SignNotifier(object):
    sign_ids = collections.defaultdict(list)

    def refresh(self, bugs, bufnr):
        if bufnr < 0:
            return

        self.bufnr = bufnr

        self._remove_signs()
        self._sign_error(bugs)

    def _sign_error(self, bugs):
        if not bugs:
            return

        seen = {}

        for i in bugs:
            if i["lnum"] <= 0 or i["lnum"] in seen:
                continue
            seen[i["lnum"]] = True

            sign_severity = "Warning" if i["type"] == 'W' else "Error"
            sign_subtype = i.get("subtype", '')
            sign_type = "Fixup{}{}".format(sign_subtype, sign_severity)

            sign_id = int(uuid.uuid4().int >> 100)

            place_sign(sign_id, i["lnum"], sign_type, i["bufnr"])

            self.sign_ids[self.bufnr].append(sign_id)

    def _remove_signs(self):
        if not hasattr(self, "bufnr"):
            return

        for i in reversed(self.sign_ids.get(self.bufnr, [])):
            unplace_sign(i, self.bufnr)
            self.sign_ids[self.bufnr].remove(i)

sign_notifier = _SignNotifier()
