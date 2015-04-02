import os.path
import time
import subprocess

from Queue import Queue
from threading import Thread


from .view import refresh_ui, Loclist, clear_notify
from .utils import get_unused_port, logging, g
from .vim_utils import (
    get_current_bufnr,
    get_filetype,
    get_fpath
)
from . import default_checkers

from .transport import event_loop, FuClient

from .checkers import load_checkers

task_queue = Queue()
worker_path = os.path.join(os.path.dirname(__file__), "worker.py")

g["refresh_cursor"] = False


def job_func(res):
    reply = res["reply"]
    logging.info("job_func {}".format(reply))

    ft = get_filetype()
    if not ft:
        return

    checker_classes = load_checkers(ft)

    loclists = []
    for c in default_checkers.get(ft, []):
        if c not in checker_classes:
            continue

        loclists.extend(reply[c])

    refresh_ui(loclists, res["bufnr"])


def checker_thread():
    port = get_unused_port()

    try:
        server = subprocess.Popen(
            ["python", worker_path, "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
    except Exception:
        raise

    limited, i = 10, 0
    while i < limited:
        client = FuClient(port)
        try:
            client.connect()
            client.server_started = True
            break
        except:
            time.sleep(0.1)
            pass
        i += 1

    if not client.server_started:
        logging.warning("Server not started, cannot connect.")

    try:
        event_loop(client, task_queue, job_func=job_func)
    except Exception as e:
        logging.exception(e)
    finally:
        client.close()
        server.terminate()


class Checker(object):
    def __init__(self):
        self._client_started = False

    def _start_client(self):
        self.client = Thread(target=checker_thread)
        self.client.start()

        self._client_started = True

    def update_errors(self):
        g["refresh_cursor"] = False

        ft = get_filetype()
        if not ft:
            return

        if ft not in default_checkers:
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
            clear_notify(self.bufnr)
        else:
            self.update_errors()

    def exit(self):
        if self._client_started and self.client.is_alive():
            task_queue.put({"cmd": "exit"})
            self.client.join()
