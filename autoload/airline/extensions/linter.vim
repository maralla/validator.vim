" vim: et ts=2 sts=2 sw=2

let g:airline#extensions#linter#enabled = 1

function! airline#extensions#linter#get_warnings()
  let errors = LinterStatusline()
  if strlen(errors) > 0
    return errors.(g:airline_symbols.space)
  endif
  return ''
endfunction

function! airline#extensions#linter#init(ext)
  call airline#parts#define_function('linter', 'airline#extensions#linter#get_warnings')
endfunction
