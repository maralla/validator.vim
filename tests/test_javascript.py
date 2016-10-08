import json
import mock
import pytest
import tempfile
import validator

from lints.javascript import EsLint, Jshint


@pytest.fixture
def none_exists(monkeypatch):
    exe_exist = mock.Mock(return_value=True)
    monkeypatch.setattr(validator, 'exe_exist', exe_exist)


def test_eslint_cmd(none_exists):
    with tempfile.NamedTemporaryFile() as fp:
        cmd = EsLint().format_cmd(fp.name)

    assert cmd == ('eslint -f compact --no-color --stdin'
                   ' --stdin-filename test_file')


def test_eslint_parse_loclist():
    loclist = ["/Users/maralla/Workspace/temp/test_js/a.js: line 1, col 10,"
               " Error - 'f' is defined but never used. (no-unused-vars)"]
    res = EsLint().parse_loclist(loclist, 1)
    assert json.loads(res)[0] == {
        "lnum": "1",
        "text": "[eslint]\'f\' is defined but never used. (no-unused-vars)",
        "enum": 1,
        "bufnr": 1,
        "warning": None,
        "error": "Error",
        "type": "E",
        "col": "10"
    }


def test_jshint_parse_loclist():
    loclist = ["/some/foo.js: line 268, col 33,"
               " eval can be harmful. (W061)"]
    res = Jshint().parse_loclist(loclist, 1)
    assert json.loads(res)[0] == {
        "lnum": "268",
        "text": "[jshint]eval can be harmful. (W061)",
        "enum": 1,
        "bufnr": 1,
        "warning": "W",
        "error": None,
        "type": "W",
        "code": "061",
        "col": "33"
    }
