" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

function! s:highlight()
    if !hlexists('LinterErrorSign')
        highlight LinterErrorSign ctermfg=88 ctermbg=235
    endif
    if !hlexists('LinterWarningSign')
        highlight LinterWarningSign ctermfg=3 ctermbg=235
    endif
    if !hlexists('LinterStyleErrorSign')
        highlight link LinterStyleErrorSign LinterErrorSign
    endif
    if !hlexists('LinterStyleWarningSign')
        highlight link LinterStyleWarningSign LinterWarningSign
    endif
    if !hlexists('LinterStyleErrorLine')
        highlight link LinterStyleErrorLine LinterErrorLine
    endif
    if !hlexists('LinterStyleWarningLine')
        highlight link LinterStyleWarningLine LinterWarningLine
    endif

    " define the signs used to display syntax and style errors/warns
    execute 'sign define LinterError text=' . g:linter_error_symbol .
        \ ' texthl=LinterErrorSign linehl=LinterErrorLine'
    execute 'sign define LinterWarning text=' . g:linter_warning_symbol .
        \ ' texthl=LinterWarningSign linehl=LinterWarningLine'
    execute 'sign define LinterStyleError text=' . g:linter_style_error_symbol .
        \ ' texthl=LinterStyleErrorSign linehl=LinterStyleErrorLine'
    execute 'sign define LinterStyleWarning text=' . g:linter_style_warning_symbol .
        \ ' texthl=LinterStyleWarningSign linehl=LinterStyleWarningLine'
endfunction


function! s:python_import()
python << EOF
from linter import Linter, g, location_list
linter = Linter()
EOF
endfunction

function! linter#intall_event_handlers()
    augroup linter
        autocmd!
        autocmd CursorMoved  * call linter#on_cursor_move()
        autocmd CursorHold   * call linter#on_cursor_hold()
        autocmd CursorHoldI  * :python linter.update_errors()
        autocmd BufReadPost  * :python linter.update_errors()
        autocmd BufWritePost * :python linter.update_errors()
        autocmd BufEnter     * :python linter.update_errors()
        autocmd VimLeave     * :python linter.exit()
    augroup END
endfunction

function! linter#enable()
    if &diff
        return
    endif

    call s:highlight()
    call s:python_import()

    command! LinterToggle :python linter.toggle()
    call linter#intall_event_handlers()

    py linter.update_errors()
endfunction

function! linter#refresh_cursor()
python << EOF
txt_map = location_list.text_map()
cursor = vim.eval("line('.')")
print(txt_map.get(cursor, ''))
EOF
endfunction

function! linter#on_cursor_move()
  let refresh_cursor = pyeval('g["refresh_cursor"]')
  if refresh_cursor
    call linter#refresh_cursor()
  endif
endfunction


function! linter#on_cursor_hold()
  py location_list.refresh()
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
