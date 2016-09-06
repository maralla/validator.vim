" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:jobs = {}

function! s:highlight()
    if !hlexists('ValidatorErrorSign')
        highlight ValidatorErrorSign ctermfg=88 ctermbg=235
    endif
    if !hlexists('ValidatorWarningSign')
        highlight ValidatorWarningSign ctermfg=3 ctermbg=235
    endif
    if !hlexists('ValidatorStyleErrorSign')
        highlight link ValidatorStyleErrorSign ValidatorErrorSign
    endif
    if !hlexists('ValidatorStyleWarningSign')
        highlight link ValidatorStyleWarningSign ValidatorWarningSign
    endif
    if !hlexists('ValidatorStyleErrorLine')
        highlight link ValidatorStyleErrorLine ValidatorErrorLine
    endif
    if !hlexists('ValidatorStyleWarningLine')
        highlight link ValidatorStyleWarningLine ValidatorWarningLine
    endif

    " define the signs used to display syntax and style errors/warns
    execute 'sign define ValidatorError text=' . g:validator_error_symbol .
        \ ' texthl=ValidatorErrorSign linehl=ValidatorErrorLine'
    execute 'sign define ValidatorWarning text=' . g:validator_warning_symbol .
        \ ' texthl=ValidatorWarningSign linehl=ValidatorWarningLine'
    execute 'sign define ValidatorStyleError text=' . g:validator_style_error_symbol .
        \ ' texthl=ValidatorStyleErrorSign linehl=ValidatorStyleErrorLine'
    execute 'sign define ValidatorStyleWarning text=' . g:validator_style_warning_symbol .
        \ ' texthl=ValidatorStyleWarningSign linehl=ValidatorStyleWarningLine'
endfunction


function validator#handler(ch)
  let msg = []
  while ch_status(a:ch) == 'buffered'
    call add(msg, ch_read(a:ch))
  endwhile
  let nr = bufnr('')

python << EOF
import validator
import vim

msg = vim.eval('msg')
bufnr = vim.eval('nr')
ftype = vim.eval('&ft')
result = []
for c in validator.cache[ftype]:
    result.extend(c.parse_loclist(msg, bufnr))
EOF

  let loclist = map(pyeval('result'), {i, v -> json_decode(v)})
  call validator#notifier#notify(loclist, nr)
endfunction


function! s:execute(cmd)
  if has_key(s:jobs, a:cmd) && job_status(s:jobs[a:cmd]) == 'run'
    job_stop(s:jobs[a:cmd])
  endif

  return job_start(a:cmd, {"close_cb": "validator#handler"})
endfunction


function! s:check()
  if empty(&filetype)
    return
  endif

  let temp = tempname() . '.' . expand('%:e')
  call writefile(getline(1, '$'), temp)

python << EOF
import validator
import vim

ftype = vim.eval('&filetype')
if validator.cache.get(ftype) is None:
    validator.cache[ftype] = list(validator.load_checkers(ftype).values())

fpath = vim.eval('temp')
cmds = [c.format_cmd(fpath) for c in validator.cache[ftype]]
EOF

  let cmds = pyeval('cmds')
  for cmd in cmds
    if empty(cmd)
      continue
    endif
    let s:jobs[cmd] = s:execute(cmd)
  endfor
endfunction


function! s:on_cursor_move()
  let nr = bufnr('')
  let line = line('.')
  let signs = get(g:sign_map, nr, {})
  echo get(signs, line, '')
endfunction


function! s:on_text_changed()
  if exists('s:timer')
    let info = timer_info(s:timer)
    if !empty(info)
      call timer_stop(s:timer)
    endif
  endif

  let s:timer = timer_start(500, {t->s:check()})
endfunction


function! s:install_event_handlers()
    augroup validator
        autocmd!
        autocmd CursorMoved  * call s:on_cursor_move()
        autocmd TextChangedI * call s:on_text_changed()
        autocmd TextChanged  * call s:on_text_changed()
        autocmd BufReadPost  * call s:check()
        autocmd BufWritePost * call s:check()
        autocmd BufEnter     * call s:check()
    augroup END
endfunction


function! validator#enable()
    if &diff
        return
    endif

    call s:highlight()

    " command! ValidatorToggle :python validator.toggle()
    call s:install_event_handlers()
    call s:check()
endfunction


function! validator#get_status_string()
  let nr = bufnr('')
  let signs = sort(map(keys(get(g:sign_map, nr, {})), {i,x->str2nr(x)}), {a,b->a==b?0:a>b?1:-1})
  return empty(signs) ? '' : '[Syntax: line:'.signs[0].' ('.len(signs).')]'
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
