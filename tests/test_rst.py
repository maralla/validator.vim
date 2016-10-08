import json
from lints.rst import RST2PseudoXMLLint


def test_rst2pseudoxml_severe_dot_regex():
    msg = [
        'Some Document.rst:355: (SEVERE/4) Unexpected section title or transition.',  # noqa
    ]

    res = RST2PseudoXMLLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "355",
        "bufnr": 1,
        "enum": 1,
        "text": u'[rst2pseudoxml.py]Unexpected section title or transition.',
        "type": "E",
        "error": "SEVERE/4",
        "warning": None,
    }


def test_rst2pseudoxml_severe_colon_regex():
    msg = [
        'Another.rst:123: (SEVERE/4) Unexpected section title or transition:',
    ]

    res = RST2PseudoXMLLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "123",
        "bufnr": 1,
        "enum": 1,
        "text": u'[rst2pseudoxml.py]Unexpected section title or transition:',
        "type": "E",
        "error": "SEVERE/4",
        "warning": None,
    }


def test_rst2pseudoxml_warning_regex():
    msg = [
        'Inte.rst:251: (WARNING/2) Title level inconsistent.'
    ]

    res = RST2PseudoXMLLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "251",
        "bufnr": 1,
        "enum": 1,
        "text": u'[rst2pseudoxml.py]Title level inconsistent.',
        "type": "W",
        "error": None,
        "warning": "WARNING/2",
    }
