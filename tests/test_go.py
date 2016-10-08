import json
from lints.go import GoFmtLint, GolintLint


def test_gofmt():
    msg = ["pythia/internal/tools/go/loader/testdata/badpkgdecl.go:1:34:"
           " expected 'package', found 'EOF'"]

    res = GoFmtLint().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "lnum": "1",
        "col": "34",
        "text": "[gofmt]expected 'package', found 'EOF'",
        "enum": 1,
        "bufnr": 1,
        "type": "E"
    }]


def test_golint():
    msg = ["pythia/internal/tools/go/loader/testdata/badpkgdecl.go:1:34:"
           " expected 'package', found 'EOF'"]

    res = GolintLint().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "lnum": "1",
        "col": "34",
        "text": "[golint]expected 'package', found 'EOF'",
        "enum": 1,
        "bufnr": 1,
        "type": "E",
    }]
