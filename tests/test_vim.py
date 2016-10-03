import json
from lints.vim import VimVint


def test_undefined_variable():
    msg = ['t.vim:3:6: Undefined variable: s:test (see :help E738)']

    res = VimVint.parse_loclist(msg, 1)
    assert json.loads(res[0]) == {
        "lnum": "3",
        "col": "6",
        "text": "[vint]Undefined variable: s:test (see :help E738)",
        "enum": 1,
        "bufnr": 1,
        "type": "E"
    }
