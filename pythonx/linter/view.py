# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .notifier import sign_notifier
from .vim_utils import get_current_bufnr
from .utils import g

STATUSLINE_FMT = "[Syntax: line:{line} ({total})]"


class _Loclist(object):
    def __init__(self):
        self.disabled = False
        self.errors = {}

    def __setitem__(self, bufnr, errors):
        self.errors[bufnr] = {"lst": errors, "_refreshed": False}

    def __getitem__(self, bufnr):
        errors = self.errors.get(bufnr, [])
        if errors:
            errors = errors["lst"]
        return errors

    def text_map(self):
        tmap = {}

        bufnr = get_current_bufnr()
        for e in self[bufnr]:
            tmap[e["lnum"]] = e["text"]
        return tmap

    def statusline_flag(self):
        bufnr = get_current_bufnr()
        errors = self[bufnr]
        if not errors:
            return ''
        return STATUSLINE_FMT.format(line=errors[0]["lnum"], total=len(errors))

    def _refresh_state(self, bufnr, state=None):
        loclist = self.errors.get(bufnr)
        if not loclist:
            s = True
        else:
            s = loclist["_refreshed"]
        if state is not None:
            loclist["_refreshed"] = state
        return s

    def refresh(self):
        bufnr = get_current_bufnr()

        if self._refresh_state(bufnr):
            return

        loclists = [] if self.disabled else self[bufnr]
        sign_notifier.refresh(loclists, bufnr)

        g["refresh_cursor"] = True

        self._refresh_state(bufnr, True)

    def clear(self, bufnr):
        self[bufnr] = []
        sign_notifier.refresh([], bufnr)

        g["refresh_cursor"] = False

location_list = _Loclist()
