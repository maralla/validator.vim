import json
from lints.zsh import ZshLint


def test_zsh():
    msg = [
        '.zshrc:598: no such file or directory: /etc/ssh/ssh_known_hosts2',
    ]

    res = ZshLint().parse_loclist(msg, 1)
    assert json.loads(res)[0] == {
        "lnum": "598",
        "bufnr": 1,
        "enum": 1,
        "text": '[zsh]no such file or directory: /etc/ssh/ssh_known_hosts2',
        "type": "E",
    }
