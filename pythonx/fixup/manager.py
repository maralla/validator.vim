# -*- coding: utf-8 -*-

from __future__ import absolute_import

from Queue import Queue
from threading import Thread

from .view import location_list
from .utils import logging, g
from .vim_utils import (
    get_current_bufnr,
    get_filetype,
    get_fpath,
)

from .checkers import load_checkers

task_queue = Queue()

g["refresh_cursor"] = False


def check(task):
    checker_classes = load_checkers(task["ft"])

    loclists = []
    for checker in checker_classes.values():
        loclists.extend(checker.gen_loclist(task["fpath"], task["bufnr"]))

    location_list[task["bufnr"]] = loclists


def checker_thread():
    while True:
        task = task_queue.get()
        if task["cmd"] == "exit":
            break

        try:
            check(task)
        except Exception as e:
            logging.exception(e)


class Checker(object):
    def __init__(self):
        self.checker = None

    def _start_checker(self):
        self.checker = Thread(target=checker_thread)
        self.checker.daemon = True
        self.checker.start()

    def update_errors(self):
        if location_list.disabled:
            return

        g["refresh_cursor"] = False

        ft = get_filetype()
        if not ft or not load_checkers(ft):
            return

        if not self.checker:
            self._start_checker()

        self.bufnr = get_current_bufnr()

        task = {"cmd": "check", "ft": ft, "fpath": get_fpath(),
                "bufnr": self.bufnr}
        task_queue.put(task)

    def toggle(self):
        location_list.disabled = not location_list.disabled
        if location_list.disabled:
            location_list.clear(self.bufnr)
        else:
            self.update_errors()

    def exit(self):
        if self.checker and self.checker.is_alive():
            task_queue.put({"cmd": "exit"})
            self.checker.join()
