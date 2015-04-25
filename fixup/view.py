# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .notifier import SignNotifier
from .vim_utils import get_current_bufnr
from .utils import g


class Loclist(object):
    statusline_fmt = "[Syntax: line:{line} ({total})]"
    errors = {}
    disabled = False

    @classmethod
    def set(cls, errors, bufnr):
        cls.errors[bufnr] = {"lst": errors, "_refreshed": False}

    @classmethod
    def get(cls, bufnr):
        errors = cls.errors.get(bufnr, [])
        if errors:
            errors = errors["lst"]
        return errors

    @classmethod
    def text_map(cls):
        tmap = {}

        bufnr = get_current_bufnr()
        errors = cls.get(bufnr)
        for e in errors:
            tmap[e["lnum"]] = e["text"]
        return tmap

    @classmethod
    def statusline_flag(cls):
        bufnr = get_current_bufnr()
        errors = cls.get(bufnr)
        if not errors:
            return ''

        return cls.statusline_fmt.format(line=errors[0]["lnum"],
                                         total=len(errors))

    @classmethod
    def _refresh_state(cls, bufnr, state=None):
        loclist = cls.errors.get(bufnr)
        if not loclist:
            s = True
        else:
            s = loclist["_refreshed"]
        if state is not None:
            loclist["_refreshed"] = state
        return s

    @classmethod
    def refresh(cls):
        bufnr = get_current_bufnr()

        if cls._refresh_state(bufnr):
            return

        loclists = cls.get(bufnr)
        loclists = [] if cls.disabled else loclists

        sign_notifier = SignNotifier()
        sign_notifier.refresh(loclists, bufnr)

        g["refresh_cursor"] = True

        cls._refresh_state(bufnr, True)

    @classmethod
    def clear(cls, bufnr):
        cls.set([], bufnr)

        sign_notifier = SignNotifier()
        sign_notifier.refresh([], bufnr)

        g["refresh_cursor"] = False
