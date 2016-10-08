import json
from lints.perl import PerlLint, PerlCriticLint


def test_perl():
    msg = ['Missing $ on loop variable at bin/foo line 26.']

    res = PerlLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "26",
        "text": "[perl]Missing $ on loop variable at bin/foo line 26.",
        "enum": 1,
        "type": "E",
        "bufnr": 1
    }


def test_perlcritic():
    msg = [
        "Subroutine prototypes used at line 989, column 1.  See page 194 of PBP.  (Severity: 5)"  # noqa
    ]

    res = PerlCriticLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "989",
        "col": "1",
        "text": '[perlcritic]Subroutine prototypes used at line 989, column 1.  See page 194 of PBP.  (Severity: 5)',  # noqa
        "enum": 1,
        "bufnr": 1,
        "type": "E",
        "code": "5",
    }
