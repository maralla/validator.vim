" vim: et ts=2 sts=2 sw=2

scriptencoding utf-8

let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
    let &cpo = s:save_cpo
    unlet s:save_cpo
endfunction

if exists('g:loaded_validator_plugin')
    call s:restore_cpo()
    finish
elseif !(has('python') || has('python3')) || !(has('job') && has('timers') && has('lambda'))
    echohl WarningMsg |
                \ echomsg 'Validator requires vim compiled with python or python3 and has features `job`, `timers` and `lambda`' |
                \ echohl None
    call s:restore_cpo()
    finish
endif


let g:_validator_sign_map = {}
let g:loaded_validator_plugin = 1
let s:validator_symbol = '∙'
let s:ignores = ['nerdtree', 'qf', 'unite', 'help', 'text']

let g:validator_error_symbol = get(g:, 'validator_error_symbol', s:validator_symbol)
let g:validator_warning_symbol = get(g:, 'validator_warning_symbol', s:validator_symbol)
let g:validator_style_error_symbol = get(g:, 'validator_style_error_symbol', g:validator_error_symbol)
let g:validator_style_warning_symbol = get(g:, 'validator_style_warning_symbol', g:validator_warning_symbol)
let g:validator_debug = get(g:, 'validator_debug', 0)
let g:validator_error_msg_format = get(g:, 'validator_error_msg_format', '● %d/%d issues')
let g:validator_auto_open_quickfix = get(g:, 'validator_auto_open_quickfix', 0)
let g:validator_filetype_map = get(g:, 'validator_filetype_map', {})
let g:validator_ignore = extend(get(g:, 'validator_ignore', []), s:ignores)
let g:validator_permament_sign = get(g:, 'validator_permament_sign', 0)
let g:validator_highlight_message = get(g:, 'validator_highlight_message', 0)


if get(g:, 'validator_autostart', 1)
    augroup validator
        autocmd!
        autocmd VimEnter * call validator#enable()
    augroup END
endif


call s:restore_cpo()

" vim: set sw=4 sts=4 et fdm=marker:
