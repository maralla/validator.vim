import functools
import vim

from . import load_checkers
from .utils import to_unicode


def _api(func):
    @functools.wraps(func)
    def wrapper():
        return func(vim.bindeval('a:'))
    return wrapper


@_api
def get_checkers(args):
    loaded = load_checkers(args['ft'])
    checkers = []
    for c in loaded.values():
        if args['instant'] and not c.instant:
            continue
        checkers.append(vim.Dictionary(
            checker=c.checker,
            cwd=c.cwd or '',
            cmd=c.format_cmd(to_unicode(args['tmp'])),
            stdin=c.stdin,
        ))
    return vim.List(checkers)


@_api
def parse_loclist(args):
    linter = load_checkers(args['ft']).get(to_unicode(args['checker']))
    msgs = [to_unicode(m) for m in args['msg']]
    return linter.parse_loclist(msgs, args['nr']) if linter else '[]'
