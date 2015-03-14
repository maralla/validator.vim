# -*- coding: utf-8 -*-

from __future__ import print_function

import collections
import vim
import uuid


class SignNotifier(object):
    sign_ids = collections.defaultdict(list)

    def refresh(self, bugs):
        self._remove_signs()
        self._sign_error(bugs)

    def _sign_error(self, bugs):
        if not bugs:
            return

        seen = {}

        for i in bugs:
            if i['lnum'] > 0 and i["lnum"] not in seen:
                seen[i["lnum"]] = True

                sign_severity = "Warning" if i["type"] == 'W' else "Error"
                sign_subtype = i.get("subtype", '')
                sign_type = "Fixup{}{}".format(sign_subtype, sign_severity)

                sign_id = int(uuid.uuid4().int >> 100)

                vim.command("sign place {} line={} name={} buffer={}".format(
                    sign_id, i["lnum"], sign_type, i["bufnr"]))

                self.sign_ids[vim.current.buffer.number].append(sign_id)

    def _remove_signs(self):
        bfnum = vim.current.buffer.number

        for i in reversed(self.sign_ids.get(bfnum, [])):
            vim.command("sign unplace {}".format(i))
            self.sign_ids[bfnum].remove(i)


class CursorNotifier(object):
    def refresh(self):
        vim.command("autocmd! fixup CursorMoved")
        self.echo_text()

    def echo_text(self):
        vim.command("autocmd fixup CursorMoved * call FixupRefreshCursor()")
