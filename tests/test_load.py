import mock
from validator import Validator, load_checkers


class Linter1(Validator):
    __filetype__ = 'linter1'

    checker = 'checker1'


class Linter2(Validator):
    __filetype__ = 'linter2'

    checker = 'checker2'


def test_load_checkers():
    import vim

    with mock.patch.dict(vim.vars, {
            'validator_filetype_map': {b'abcd': b'linter1'}}):
        assert isinstance(load_checkers(b'abcd')['checker1'], Linter1)
    assert isinstance(load_checkers(b'linter2')['checker2'], Linter2)
