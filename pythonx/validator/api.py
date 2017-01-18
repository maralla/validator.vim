import functools
import vim

from . import load_checkers


def _api(func):
    @functools.wraps(func)
    def wrapper():
        return func(vim.bindeval('a:'))
    return wrapper


@_api
def get_checkers(args):
    loaded = load_checkers(args['ft'])
    return [(c.checker, c.format_cmd(args['tmp']), c.stdin)
            for c in loaded.values()]


@_api
def parse_loclist(args):
    linter = load_checkers(args['ft']).get(args['checker'])
    return linter.parse_loclist(args['msg'], args['nr']) if linter else '[]'
