import json
from lints.vim import VimVint, VimLParserLint


def test_vint_undefined_variable():
    msg = ['t.vim:3:6: Undefined variable: s:test (see :help E738)']

    res = VimVint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "3",
        "col": "6",
        "text": "[vint]Undefined variable: s:test (see :help E738)",
        "enum": 1,
        "bufnr": 1,
        "type": "E"
    }


def test_vimlparser_message_wihtout_code():
    msg = ['CCTree/plugin/cctree.vim:549:18: vimlparser: unexpected EOL']

    res = VimLParserLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "549",
        "col": "18",
        "text": '[vimlparser]unexpected EOL',
        "enum": 1,
        "bufnr": 1,
        "type": "E",
        "code": None,
        "error": None,
        "warning": None,
    }


def test_vimlparser_message_with_code():
    msg = ['vim-unite-vcs/autoload/vcs/git/revert.vim:29:19: vimlparser: E488: Trailing characters: )']  # noqa

    res = VimLParserLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "29",
        "col": "19",
        "text": '[vimlparser]E488: Trailing characters: )',
        "enum": 1,
        "bufnr": 1,
        "type": "E",
        "code": "488",
        "error": "E",
        "warning": None,
    }
