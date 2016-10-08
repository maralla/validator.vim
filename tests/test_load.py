from validator import Validator, load_checkers


class Linter1(Validator):
    __filetype__ = 'linter1'

    checker = 'checker1'


class Linter2(Validator):
    __filetype__ = 'linter2'

    checker = 'checker2'


def test_load_checkers(monkeypatch):
    import vim

    monkeypatch.setattr(vim, "eval", lambda x: {"abcd": "linter1"})

    assert isinstance(load_checkers("abcd")['checker1'], Linter1)
    assert isinstance(load_checkers("linter2")['checker2'], Linter2)
