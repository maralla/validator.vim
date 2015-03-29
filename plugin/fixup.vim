" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
    let &cpo = s:save_cpo
    unlet s:save_cpo
endfunction

if exists("g:loaded_fixup_plugin")
    call s:restore_cpo()
    finish
elseif !has('python')
    echohl WarningMsg |
                \ echomsg "Fixup requires vim compiled with python" |
                \ echohl None
    call s:restore_cpo()
    finish
endif

let g:loaded_fixup_plugin = 1


let s:fixup_symbol = '●'

let g:fixup_error_symbol =
            \ get(g:, "fixup_error_symbol", s:fixup_symbol)
let g:fixup_warning_symbol =
            \ get(g:, "fixup_warning_symbol", s:fixup_symbol)
let g:fixup_style_error_symbol =
            \ get(g:, "fixup_style_error_symbol", g:fixup_error_symbol)
let g:fixup_style_warning_symbol =
            \ get(g:, "fixup_style_warning_symbol", g:fixup_warning_symbol)


function! FixupStatusline()
    py from fixup.view import Loclist
    return pyeval('Loclist.statusline_flag()')
endfunction

augroup fixup
    autocmd!
    autocmd VimEnter * call fixup#enable()
augroup END


call s:restore_cpo()

" vim: set sw=4 sts=4 et fdm=marker:
