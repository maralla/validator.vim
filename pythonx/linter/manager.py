# -*- coding: utf-8 -*-

from __future__ import absolute_import

import tempfile
import os

from Queue import Queue
from threading import Thread

from .view import location_list
from .utils import logging, g
from .vim_utils import (
    get_current_bufnr,
    get_filetype,
    save
)

from .checker import load_checkers

task_queue = Queue()

g["refresh_cursor"] = False


def check(task):
    checker_classes = load_checkers(task["ft"])

    loclists = []
    for checker in checker_classes.values():
        loclists.extend(checker.gen_loclist(task["fpath"], task["bufnr"]))

    location_list[task["bufnr"]] = loclists


def linter_thread():
    while True:
        task = task_queue.get()
        if task["cmd"] == "exit":
            break

        try:
            check(task)
        except Exception as e:
            logging.exception(e)


class Linter(object):
    def __init__(self):
        _, self.temp_file = tempfile.mkstemp(prefix="vim-linter")
        self.linter = None

    def _start_linter(self):
        self.linter = Thread(target=linter_thread)
        self.linter.daemon = True
        self.linter.start()

    def _save_file(self):
        save(self.temp_file)

    def update_errors(self):
        if location_list.disabled:
            return

        g["refresh_cursor"] = False

        ft = get_filetype()
        if not ft or not load_checkers(ft):
            return

        if not self.linter:
            self._start_linter()

        self.bufnr = get_current_bufnr()

        self._save_file()

        task = {"cmd": "check", "ft": ft, "fpath": self.temp_file,
                "bufnr": self.bufnr}
        task_queue.put(task)

    def toggle(self):
        location_list.disabled = not location_list.disabled
        if location_list.disabled:
            location_list.clear(self.bufnr)
        else:
            self.update_errors()

    def exit(self):
        try:
            os.remove(self.temp_file)
        except OSError:
            pass

        if self.linter and self.linter.is_alive():
            task_queue.put({"cmd": "exit"})
            self.linter.join()
