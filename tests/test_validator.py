import json
import tempfile

from validator import Validator


class NoName(Validator):
    __filetype__ = 'no-name'

    checker = "ls"
    args = "-a -b -c -d"
    regex = r"""
            (?P<lnum>\d+):
            (?P<col>\d+)
            \s
            (?P<type>\w+):
            \s
            (?P<text>.*)"""


def test_parse_loclist():
    loclist = [
        'hello world',
        '123:45 error: hello wrold',
        '456:9 warning: abcd'
    ]

    data = [json.loads(l) for l in NoName.parse_loclist(loclist, 1)]
    assert data == [
        {
            "lnum": "123",
            "text": "hello wrold",
            "enum": 2,
            "type": "E",
            "col": "45",
            "bufnr": 1
        },
        {
            "lnum": "456",
            "text": "abcd",
            "enum": 3,
            "type": "W",
            "col": "9",
            "bufnr": 1
        }
    ]


def test_format_cmd():
    with tempfile.NamedTemporaryFile() as fp:
        cmd = NoName.format_cmd(fp.name)

    assert cmd == 'ls -a -b -c -d {}'.format(fp.name)
