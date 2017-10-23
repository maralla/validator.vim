let s:py = has('python3') ? 'py3' : 'py'
let s:pyeval = function(has('python3') ? 'py3eval' : 'pyeval')


function! validator#utils#setup_python()
  exe s:py 'from validator import api as validator_api'
endfunction


function! validator#utils#load_checkers(ft, tmp, instant)
  exe s:py 'res = validator_api.get_checkers()'
  return s:pyeval('res')
endfunction


function! validator#utils#parse_loclist(msg, nr, ft, checker)
  exe s:py 'res = validator_api.parse_loclist()'
  return json_decode(s:pyeval('res'))
endfunction
