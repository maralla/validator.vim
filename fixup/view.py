# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .notifier import SignNotifier, CursorNotifier
from .vim_utils import get_current_bufnr, cursor_jump


class Loclist(object):
    statusline_fmt = "[Syntax: line:{line} ({total})]"
    errors = {}
    disabled = False

    @classmethod
    def set(cls, errors, bufnr):
        cls.errors[bufnr] = errors

    @classmethod
    def text_map(cls):
        tmap = {}

        bufnr = get_current_bufnr()
        for e in cls.errors.get(bufnr, []):
            tmap[e["lnum"]] = e["text"]
        return tmap

    @classmethod
    def statusline_flag(cls):
        bufnr = get_current_bufnr()
        errors = cls.errors.get(bufnr)
        if not errors:
            return ''

        return cls.statusline_fmt.format(line=errors[0]["lnum"],
                                         total=len(errors))


def clear_notify(bufnr):
    Loclist.set([], bufnr)

    sign_notifier = SignNotifier()
    sign_notifier.refresh([])

    cursor_notifier = CursorNotifier()
    cursor_notifier.refresh()


def refresh_ui(loclists, bufnr):
    loclists = [] if Loclist.disabled else loclists

    Loclist.set(loclists, bufnr)

    sign_notifier = SignNotifier()
    sign_notifier.refresh(loclists, bufnr)

    cursor_notifier = CursorNotifier()
    cursor_notifier.refresh()

    if loclists:
        cursor_jump(int(loclists[0]["lnum"]), int(loclists[0].get("col", 1)))

    return loclists
