import json
from lints.lua import LuaCLint, LuacheckLint


def test_luac():
    msg = ['luac: /tmp/foo.lua:16: syntax error near <eof>']

    res = LuaCLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "16",
        "text": "[luac]syntax error near <eof>",
        "enum": 1,
        "bufnr": 1,
        "type": "E"
    }


def test_luacheck():
    msg = ["    /tmp/foo.lua:16:1: expected '=' near <eof>"]

    res = LuacheckLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "16",
        "col": "1",
        "text": "[luacheck]expected '=' near <eof>",
        "enum": 1,
        "bufnr": 1,
        "type": "E"
    }
