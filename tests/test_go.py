import json
from lints.go import GoFmtLint, GolintLint, Gometalinter


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


def test_gometalinter():
    msg = [
        "../../../../../../../private/var/folders/4q/k3d4z8tx03j7wx5wg0y"
        "1py7c0000gp/T/vn7xYjh/temp2.go:1:1:error: expected 'package', "
        "found 'IDENT' a (gotype)"
    ]
    res = Gometalinter().parse_loclist(msg, 1)
    assert json.loads(res) == [{
        "col": "1",
        "lnum": "1",
        "error": "error",
        "bufnr": 1,
        "enum": 1,
        "warning": None,
        "text": "[gometalinter]expected 'package', found 'IDENT' a (gotype)",
        "type": "E"
    }]
