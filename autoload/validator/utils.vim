function validator#utils#option(type, ft, checker)
  if !has_key(g:validator_option, a:type)
    let g:validator_option[a:type] = {}
  endif

  if !has_key(g:validator_option[a:type], a:ft)
    let g:validator_option[a:type][a:ft] = {}
  endif

  return get(g:validator_option[a:type][a:ft], a:checker, '')
endfunction
