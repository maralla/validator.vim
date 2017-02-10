import json
from lints.go import GoFmtLint, GolintLint, GoMetalinterLint


def test_gometalinter():
    msgs = ["main.go:3:8:warning: unused struct field rune literal not "
            "terminated (and 1 more errors) (structcheck)",
            "/foo/main.go:10::warning: declaration of \"x\" shadows "
            "declaration at main.go:6 (vetshadow)"]

    res = GoMetalinterLint().parse_loclist(msgs, 1)
    assert json.loads(res)[0] == {
        "lnum": "3",
        "col": "8",
        "text": '[gometalinter]unused struct field rune literal not terminated (and 1 more errors) (structcheck)',
        "bufnr": 1,
        "type": "W",
        "enum": 1,
        "error": None,
        "warning": "warning"
    }
    assert json.loads(res)[1] == {
        "lnum": "10",
        "col": None,
        "text": '[gometalinter]declaration of "x" shadows declaration at main.go:6 (vetshadow)',
        "bufnr": 1,
        "type": "W",
        "enum": 2,
        "error": None,
        "warning": "warning"
    }


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
