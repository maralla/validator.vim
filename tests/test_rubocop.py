import json
from lints.ruby import Rubocop

def test_rubocop_error():
    msg = ['E: 1: 3: unexpected token kEND']

    res = Rubocop().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "lnum": "1",
        "col": "3",
        "text": "[rubocop]unexpected token kEND",
        "enum": 1,
        "bufnr": 1,
        "type": "E",
        "error": "E",
        "warning": None
    }]

def test_rubocop_warning():
    msg = ['W: 1: 3: end at 4, 4 is not aligned with if at 2, 2']

    res = Rubocop().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "lnum": "1",
        "col": "3",
        "text": "[rubocop]end at 4, 4 is not aligned with if at 2, 2",
        "enum": 1,
        "bufnr": 1,
        "type": "W",
        "error": None,
        "warning": "W"
    }]

def test_rubocop_style():
    msg = [u'C:  1: 3: Extra empty line detected at class body end']

    res = Rubocop().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "lnum": "1",
        "col": "3",
        "text": "[rubocop]Extra empty line detected at class body end",
        "enum": 1,
        "bufnr": 1,
        "type": "W",
        "error": None,
        "warning": "C"
    }]
