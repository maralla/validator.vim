" vim: et ts=2 sts=2 sw=2

let g:airline#extensions#fixup#enabled = 1

function! airline#extensions#fixup#get_warnings()
  let errors = FixupStatusline()
  if strlen(errors) > 0
    return errors.(g:airline_symbols.space)
  endif
  return ''
endfunction

function! airline#extensions#fixup#init(ext)
  call airline#parts#define_function('fixup', 'airline#extensions#fixup#get_warnings')
endfunction
