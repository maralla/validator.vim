import json
from lints.ruby import Ruby


def test_ruby():
    msg = [
        'app/models/message:50: syntax error, unexpected end-of-input, expecting keyword_end',
    ]

    res = Ruby().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "50",
        "bufnr": 1,
        "enum": 1,
        "text": '[ruby]syntax error, unexpected end-of-input, expecting keyword_end',
        "type": "E",
    }

