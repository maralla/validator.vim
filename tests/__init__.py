import sys
import types


def _eval(v):
    return 0

vim = types.ModuleType('vim')
vim.eval = _eval
vim.vars = {}

sys.path.append('./pythonx')
sys.modules['vim'] = vim
