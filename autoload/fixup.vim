" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:python_path = expand('<sfile>:p:h')

function! s:highlight()
    if !hlexists('FixupErrorSign')
        highlight FixupErrorSign ctermfg=88 ctermbg=235
    endif
    if !hlexists('FixupWarningSign')
        highlight FixupWarningSign ctermfg=3 ctermbg=235
    endif
    if !hlexists('FixupStyleErrorSign')
        highlight link FixupStyleErrorSign FixupErrorSign
    endif
    if !hlexists('FixupStyleWarningSign')
        highlight link FixupStyleWarningSign FixupWarningSign
    endif
    if !hlexists('FixupStyleErrorLine')
        highlight link FixupStyleErrorLine FixupErrorLine
    endif
    if !hlexists('FixupStyleWarningLine')
        highlight link FixupStyleWarningLine FixupWarningLine
    endif

    " define the signs used to display syntax and style errors/warns
    execute 'sign define FixupError text=' . g:fixup_error_symbol .
        \ ' texthl=FixupErrorSign linehl=FixupErrorLine'
    execute 'sign define FixupWarning text=' . g:fixup_warning_symbol .
        \ ' texthl=FixupWarningSign linehl=FixupWarningLine'
    execute 'sign define FixupStyleError text=' . g:fixup_style_error_symbol .
        \ ' texthl=FixupStyleErrorSign linehl=FixupStyleErrorLine'
    execute 'sign define FixupStyleWarning text=' . g:fixup_style_warning_symbol .
        \ ' texthl=FixupStyleWarningSign linehl=FixupStyleWarningLine'
endfunction


function! s:python_import()
python << EOF
import sys
import os.path
import vim

cwd = vim.eval("s:python_path")
sys.path.append(os.path.dirname(cwd))
from fixup.manager import Checker, g
from fixup.view import Loclist

checker = Checker()
EOF
endfunction

function! fixup#intall_event_handlers()
    augroup fixup
        autocmd!
        autocmd CursorMoved  * call fixup#on_cursor_move()
        autocmd CursorHold   * call fixup#on_cursor_hold()
        autocmd BufReadPost  * :python checker.update_errors()
        autocmd BufWritePost * :python checker.update_errors()
        autocmd BufEnter     * :python checker.update_errors()
        autocmd VimLeave     * :python checker.exit()
    augroup END
endfunction

function! fixup#enable()
    if &diff
        return
    endif

    call s:highlight()
    call s:python_import()

    command! FixupToggle :python checker.toggle()
    call fixup#intall_event_handlers()

    py checker.update_errors()
endfunction

function! fixup#refresh_cursor()
python << EOF
from fixup.vim_utils import get_cursor_line
txt_map = Loclist.text_map()

cursor = get_cursor_line()

print(txt_map.get(cursor, ''))
EOF
endfunction

function! fixup#on_cursor_move()
  let refresh_cursor = pyeval('g["refresh_cursor"]')
  if refresh_cursor
    call fixup#refresh_cursor()
  endif
endfunction


function! fixup#on_cursor_hold()
  py Loclist.refresh()
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
