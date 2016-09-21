" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:jobs = {}
let s:cmd_count = 0
let s:loclist = []


function s:handle(ch, checker)
  let msg = []
  while ch_status(a:ch) == 'buffered'
    call add(msg, ch_read(a:ch))
  endwhile
  let nr = bufnr('')

Py << EOF
import validator, vim
msg, bufnr, ftype, checker = map(vim.eval, ('msg', 'nr', '&ft', 'a:checker'))
ftype = ftype.split('.')[0]
c = validator.cache[ftype].get(checker)
result = c.parse_loclist(msg, bufnr) if c else []
EOF

  let s:loclist += map(Pyeval('result'), {i, v -> json_decode(v)})
  let s:cmd_count -= 1
  if s:cmd_count <= 0
    call validator#notifier#notify(s:loclist, nr)
    let s:loclist = []
  endif

endfunction


function! s:execute(cmd, checker)
  if has_key(s:jobs, a:cmd) && job_status(s:jobs[a:cmd]) == 'run'
    job_stop(s:jobs[a:cmd])
  endif

  return job_start(a:cmd, {"close_cb": {c->s:handle(c, a:checker)}, "in_io": 'null', "err_io": 'out'})
endfunction


function! s:clear()
  let s:loclist = []
  call validator#notifier#notify(s:loclist, bufnr(''))
endfunction


function! s:check()
  if empty(&filetype)
    call s:clear()
    return
  endif

  let temp = tempname() . '.' . expand('%:e')
  let lines = getline(1, '$')
  if len(lines) == 1 && empty(lines[0])
    call s:clear()
    return
  endif
  call writefile(lines, temp)

Py << EOF
import validator, vim
ftype = vim.eval('&ft').split('.')[0]
if validator.cache.get(ftype) is None:
    checkers = vim.eval("get(g:, 'validator_{}_checkers')".format(ftype))
    loaded = validator.load_checkers(ftype, checkers)
    validator.cache[ftype] = loaded

fpath = vim.eval('temp')
cmds = [(c.checker, c.format_cmd(fpath)) for c in validator.cache[ftype].values()]
EOF

  let cmds = Pyeval('cmds')
  let s:cmd_count = len(cmds)

  for [checker, cmd] in cmds
    if empty(cmd)
      let s:cmd_count -= 1
      continue
    endif
    let s:jobs[cmd] = s:execute(cmd, checker)
  endfor
endfunction


function! s:on_cursor_move()
  let nr = bufnr('')
  let line = line('.')
  let signs = get(g:sign_map, nr, {})
  echo get(signs, line, '')
endfunction


function! s:stop_timer()
  if exists('s:timer')
    let info = timer_info(s:timer)
    if !empty(info)
      call timer_stop(s:timer)
    endif
  endif
endfunction


function! s:on_text_changed()
  call s:stop_timer()
  let s:timer = timer_start(800, {t->s:check()})
endfunction


function! s:do_check()
  call s:stop_timer()
  call s:check()
endfunction


function! s:install_event_handlers()
    augroup validator
        autocmd!
        autocmd CursorMoved  * call s:on_cursor_move()
        autocmd TextChangedI * call s:on_text_changed()
        autocmd TextChanged  * call s:on_text_changed()
        autocmd BufReadPost  * call s:do_check()
        autocmd BufWritePost * call s:do_check()
    augroup END
endfunction


function! s:define_sign(type, symbol)
  exe 'sign define Validator'.a:type.' text='.a:symbol.' texthl=Validator'.a:type.'Sign'
endfunction


function! s:highlight()
  hi! ValidatorErrorSign ctermfg=88 ctermbg=235
  hi! ValidatorWarningSign ctermfg=3 ctermbg=235
  hi! link ValidatorStyleErrorSign ValidatorErrorSign
  hi! link ValidatorStyleWarningSign ValidatorWarningSign

  call s:define_sign('Error', g:validator_error_symbol)
  call s:define_sign('Warning', g:validator_warning_symbol)
  call s:define_sign('StyleError', g:validator_style_error_symbol)
  call s:define_sign('StyleWarning', g:validator_style_warning_symbol)
endfunction


function! validator#enable()
    if &diff
        return
    endif

    call s:highlight()
    call s:install_event_handlers()
    call s:check()
endfunction


function! validator#get_status_string()
  let nr = bufnr('')
  let signs = sort(map(keys(get(g:sign_map, nr, {})), {i,x->str2nr(x)}), {a,b->a==b?0:a>b?1:-1})
  return empty(signs) ? '' : printf(g:validator_error_msg_format, signs[0], len(signs))
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
