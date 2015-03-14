# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib
import vim

from . import default_checkers
from .checkers import SyntaxChecker
from .notifier import SignNotifier, CursorNotifier


statusline_fmt = "[Syntax: line:{line} ({total})]"


class Loclist(object):
    errors = []
    disabled = False

    @classmethod
    def set(cls, errors):
        cls.errors = errors

    @classmethod
    def text_map(cls):
        tmap = {}
        for e in cls.errors:
            tmap[e["lnum"]] = e["text"]
        return tmap


def toggle():
    Loclist.disabled = not Loclist.disabled
    if Loclist.disabled:
        clear_notify()
    else:
        update_errors()


def statusline_flag():
    if not Loclist.errors:
        return ''

    errors = Loclist.errors
    error_flags = statusline_fmt.format(line=errors[0]["lnum"],
                                        total=len(errors))
    return error_flags


def clear_notify():
    Loclist.set([])

    sign_notifier = SignNotifier()
    sign_notifier.refresh([])

    cursor_notifier = CursorNotifier()
    cursor_notifier.refresh()


def update_errors():
    errors = [] if Loclist.disabled else get_errors()

    Loclist.set(errors)

    sign_notifier = SignNotifier()
    sign_notifier.refresh(errors)

    cursor_notifier = CursorNotifier()
    cursor_notifier.refresh()

    if errors:
        vim.command("silent! lrewind {}".format(errors[0]["enum"]))

    return errors


def get_errors():
    checker_manager = SyntaxChecker()

    ft = vim.eval("&filetype")
    if ft == '':
        vim.command("silent! filetype detect")
        ft = vim.eval("&filetype")

    if not ft:
        return []

    if ft not in checker_manager:
        try:
            importlib.import_module("fixup.checkers.{}".format(ft))
        except ImportError:
            return []

    checker_classes = checker_manager[ft]

    errors = []
    for c in default_checkers.get(ft, []):
        if c not in checker_classes:
            continue

        try:
            errors.extend(checker_classes[c].get_loclist())
        except Exception:
            pass
    return errors
