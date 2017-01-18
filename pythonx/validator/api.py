import functools
import vim

from . import load_checkers


def _u(ft):
    if isinstance(ft, bytes):
        return ft.decode('utf-8')
    return ft


def _api(func):
    @functools.wraps(func)
    def wrapper():
        return func(vim.bindeval('a:'))
    return wrapper


@_api
def get_checkers(args):
    loaded = load_checkers(_u(args['ft']))
    return [(c.checker, c.format_cmd(_u(args['tmp'])), c.stdin)
            for c in loaded.values()]


@_api
def parse_loclist(args):
    linter = load_checkers(_u(args['ft'])).get(_u(args['checker']))
    msgs = [_u(m) for m in args['msg']]
    return linter.parse_loclist(msgs, args['nr']) if linter else '[]'
