import json
import mock
import pytest
import tempfile
import validator

from lints.javascript import EsLint


@pytest.fixture
def none_exists(monkeypatch):
    exe_exist = mock.Mock(return_value=True)
    monkeypatch.setattr(validator, 'exe_exist', exe_exist)


def test_eslint_cmd(none_exists):
    with tempfile.NamedTemporaryFile() as fp:
        cmd = EsLint.format_cmd(fp.name)

    assert cmd == 'eslint -f compact --no-color  {}'.format(fp.name)


def test_eslint_parse_loclist():
    loclist = ["/Users/maralla/Workspace/temp/test_js/a.js: line 1, col 10,"
               " Error - 'f' is defined but never used. (no-unused-vars)"]
    res = EsLint.parse_loclist(loclist, 1)
    assert json.loads(res[0]) == {
        "lnum": "1",
        "text": "[eslint]\'f\' is defined but never used. (no-unused-vars)",
        "enum": 1,
        "bufnr": 1,
        "warning": None,
        "error": "Error",
        "type": "E",
        "col": "10"
    }
