function! validator#utils#load_checkers(ft, tmp)
Py << EOF
import validator, vim
loaded = validator.load_checkers(vim.eval('a:ft'))
cmds = [(c.checker, c.format_cmd(vim.eval('a:tmp')), c.stdin) for c in loaded.values()]
EOF
  return Pyeval('cmds')
endfunction


function! validator#utils#parse_loclist(msg, nr, ft, checker)
Py << EOF
msg, bufnr, ftype, checker = map(vim.eval, ('a:msg', 'a:nr', 'a:ft', 'a:checker'))
linter = validator.load_checkers(ftype).get(checker)
result = linter.parse_loclist(msg, bufnr) if linter else '[]'
EOF
  return json_decode(Pyeval('result'))
endfunction
