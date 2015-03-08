if exists("g:loaded_fixup_plugin")
    finish
endif
let g:loaded_fixup_plugin = 1

for s:feature in [
            \ 'python',
        \ ]
    if !has(s:feature)
        echomsg "fixup: error: need Vim compiled with feature " . s:feature)
        finish
    endif
endfor


if !hlexists('FixupErrorSign')
    highlight link FixupErrorSign error
endif
if !hlexists('FixupWarningSign')
    highlight link FixupWarningSign todo
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

augroup fixup
augroup END

python << EOF

import sys
import os.path
import vim

cwd = vim.eval("expand('<sfile>:p:h')")
sys.path.append(os.path.dirname(cwd))
import fixup.checker as checker

EOF

augroup fixup
    autocmd BufReadPost  * :python checker.update_errors()
    autocmd BufWritePost * :python checker.update_errors()
    " autocmd BufEnter     * :python checker.update_errors()
augroup END

" vim: set sw=4 sts=4 et fdm=marker:
