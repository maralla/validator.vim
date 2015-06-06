# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib

from Queue import Queue
from threading import Thread

from .view import Loclist
from .utils import logging, g
from .vim_utils import (
    get_current_bufnr,
    get_filetype,
    get_fpath,
)

from .checkers import load_checkers, SyntaxChecker

task_queue = Queue()

g["refresh_cursor"] = False

checker_manager = SyntaxChecker()


def check(task):
    ft = task["ft"]
    if ft not in checker_manager:
        try:
            importlib.import_module("fixup.checkers.{}".format(ft))
        except ImportError as e:
            logging.exception(e)
            return {}

    checker_classes = checker_manager[ft]

    errors = {}
    for checker_name, checker in checker_classes.items():
        errors[checker_name] = checker.gen_loclist(
            task["fpath"], task["bufnr"])

    logging.info("check {}".format(errors))

    return errors


def job_func(ft, bufnr, res):
    checker_classes = load_checkers(ft)

    loclists = []
    for c in checker_classes:
        loclists.extend(res[c])

    Loclist.set(loclists, bufnr)


def checker_thread():
    while True:
        task = task_queue.get()
        if task["cmd"] == "exit":
            break

        ft = task["ft"]
        bufnr = task["bufnr"]

        try:
            job_func(ft, bufnr, check(task))
        except Exception as e:
            logging.exception(e)


class Checker(object):
    def __init__(self):
        self._client_started = False

    def _start_client(self):
        self.client = Thread(target=checker_thread)
        self.client.daemon = True
        self.client.start()

        self._client_started = True

    def update_errors(self):
        if Loclist.disabled:
            return

        g["refresh_cursor"] = False

        ft = get_filetype()
        if not ft or not load_checkers(ft):
            return

        if not self._client_started:
            self._start_client()

        self.bufnr = get_current_bufnr()

        task = {"cmd": "check", "ft": ft, "fpath": get_fpath(),
                "bufnr": self.bufnr}
        logging.info("task {}".format(task))
        task_queue.put(task)

    def toggle(self):
        Loclist.disabled = not Loclist.disabled
        if Loclist.disabled:
            Loclist.clear(self.bufnr)
        else:
            self.update_errors()

    def exit(self):
        if self._client_started and self.client.is_alive():
            task_queue.put({"cmd": "exit"})
            self.client.join()
