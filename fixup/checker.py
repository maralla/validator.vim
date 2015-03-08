# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib
import vim

from . import default_checkers
from .checkers import SyntaxChecker
from .notifier import SignNotifier, CursorNotifier


def update_errors():
    checker_manager = SyntaxChecker()

    ft = vim.eval("&filetype")
    if ft == '':
        vim.command("silent! filetype detect")
        ft = vim.eval("&filetype")

    if not ft:
        return

    if ft not in checker_manager:
        try:
            importlib.import_module("fixup.checkers.{}".format(ft))
        except ImportError:
            return

    checker_classes = checker_manager[ft]

    errors = []
    for c in default_checkers.get(ft, []):
        if c not in checker_classes:
            continue

        try:
            errors.extend(checker_classes[c].get_loclist())
        except Exception:
            raise
            pass

    sign_notifier = SignNotifier()
    sign_notifier.refresh(errors)

    cursor_notifier = CursorNotifier(errors)
    cursor_notifier.refresh()

    if errors:
        vim.command("silent! lrewind {}".format(errors[0]["nr"]))

    return errors
