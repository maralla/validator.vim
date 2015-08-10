" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
    let &cpo = s:save_cpo
    unlet s:save_cpo
endfunction

if exists("g:loaded_linter_plugin")
    call s:restore_cpo()
    finish
elseif !has('python')
    echohl WarningMsg |
                \ echomsg "Linter requires vim compiled with python" |
                \ echohl None
    call s:restore_cpo()
    finish
endif

let g:loaded_linter_plugin = 1


let s:linter_symbol = '●'

let g:linter_error_symbol =
            \ get(g:, "linter_error_symbol", s:linter_symbol)
let g:linter_warning_symbol =
            \ get(g:, "linter_warning_symbol", s:linter_symbol)
let g:linter_style_error_symbol =
            \ get(g:, "linter_style_error_symbol", g:linter_error_symbol)
let g:linter_style_warning_symbol =
            \ get(g:, "linter_style_warning_symbol", g:linter_warning_symbol)

let g:linter_debug = get(g:, "linter_debug", 0)


function! LinterStatusline()
    py from linter import location_list
    return pyeval('location_list.statusline_flag()')
endfunction

augroup linter
    autocmd!
    autocmd VimEnter * call linter#enable()
augroup END


call s:restore_cpo()

" vim: set sw=4 sts=4 et fdm=marker:
