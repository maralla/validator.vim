import json
from lints.sh import ShLint, ShellcheckLint


def test_regex():
    msg = [
        '__validator_temp__.sh: line 10: syntax error: unexpected end of file',
    ]

    res = ShLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "10",
        "text": "[sh]syntax error: unexpected end of file",
        "enum": 1,
        "type": "E",
        "bufnr": 1
    }


def test_shellcheck_regex():
    msg = [
        "hello.sh:6:1: error: Did you forget the 'then' for this 'if'? [SC1049]",  # noqa
    ]

    res = ShellcheckLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "6",
        "text": "[shellcheck]Did you forget the \'then\' for this \'if\'? [SC1049]",  # noqa
        "enum": 1,
        "bufnr": 1,
        "warning": None,
        "error": "error",
        "type": "E",
        "col": "1"
    }
