" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
    let &cpo = s:save_cpo
    unlet s:save_cpo
endfunction

if exists("g:loaded_validator_plugin")
    call s:restore_cpo()
    finish
elseif !(has('python') || has('python3')) || !(has('job') && has('timers') && has('lambda'))
    echohl WarningMsg |
                \ echomsg "Validator requires vim compiled with python or python3 and has features `job`, `timers` and `lambda`" |
                \ echohl None
    call s:restore_cpo()
    finish
endif


let g:sign_map = {}
let g:loaded_validator_plugin = 1
let s:validator_symbol = '∙'

let g:validator_error_symbol = get(g:, "validator_error_symbol", s:validator_symbol)
let g:validator_warning_symbol = get(g:, "validator_warning_symbol", s:validator_symbol)
let g:validator_style_error_symbol = get(g:, "validator_style_error_symbol", g:validator_error_symbol)
let g:validator_style_warning_symbol = get(g:, "validator_style_warning_symbol", g:validator_warning_symbol)
let g:validator_debug = get(g:, "validator_debug", 0)

if has("python3")
    command! -nargs=1 Py py3 <args>
    function! Pyeval(arg)
        return py3eval(a:arg)
    endfunction
else
    command! -nargs=1 Py py <args>
    function! Pyeval(arg)
        return pyeval(a:arg)
    endfunction
endif

augroup validator
    autocmd!
    autocmd VimEnter * call validator#enable()
augroup END


call s:restore_cpo()

" vim: set sw=4 sts=4 et fdm=marker:
