import sys
import types


eval_map = {
    'g:validator_filetype_map': {}
}


def _eval(v):
    return eval_map.get(v, 0)

vim = types.ModuleType('vim')
vim.eval = _eval
vim.vars = {}

sys.path.append('./pythonx')
sys.modules['vim'] = vim
