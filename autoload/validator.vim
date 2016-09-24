" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:loclist = []
let s:files = {}

let s:manager = {'refcount': 0, 'tempfile': '', 'jobs': []}

function s:manager.add_job(job)
  if job_status(a:job) == 'run'
    call add(self.jobs, a:job)
    let self.refcount += 1
  endif
endfunction

function s:manager.reset_jobs()
  for job in self.jobs
    if job_status(job) == 'run'
      call job_stop(job)
      call self.decref()
    endif
  endfor
  let self.jobs = []
endfunction

function s:manager.decref()
  let self.refcount -= 1
  if self.refcount <= 0
    try
      call delete(self.tempfile)
      call remove(s:file, self.tempfile)
    catch
    endtry
    let self.tempfile = ''
    let self.refcount = 0
  endif
endfunction


function s:handle(ch, ft, nr, checker)
  call s:manager.decref()

  let msg = []
  while ch_status(a:ch) == 'buffered'
    call add(msg, ch_read(a:ch))
  endwhile

  if bufwinnr(a:nr) == -1
    return
  endif

Py << EOF
msg, bufnr, ftype, checker = map(vim.eval, ('msg', 'a:nr', 'a:ft', 'a:checker'))
linter = validator.load_checkers(ftype).get(checker)
result = linter.parse_loclist(msg, bufnr) if linter else []
EOF

  let s:loclist += map(Pyeval('result'), {i, v -> json_decode(v)})
  if s:manager.refcount <= 0
    call validator#notifier#notify(s:loclist, a:nr)
    let s:loclist = []
  endif

endfunction


function! s:clear(nr)
  let s:loclist = []
  call validator#notifier#notify(s:loclist, a:nr)
endfunction


function! s:check()
  let ft = &filetype
  if index(g:validator_ignore, ft) != -1
    return
  endif

  call s:manager.reset_jobs()

  let nr = bufnr('')
  let name = expand('%:t')

  if empty(ft) || empty(name)
    call s:clear(nr)
    return
  endif

  let ext = expand('%:e')
  let ext = empty(ext) ? '' : '.'.ext

  let s:manager.tempfile = fnamemodify(expand('%:p'), ':s/'.name.'$/__validator_temp__'.ext.'/')
  let tmp = s:manager.tempfile

  let lines = getline(1, '$')
  if len(lines) == 1 && empty(lines[0])
    call s:clear(nr)
    return
  endif

Py << EOF
loaded = validator.load_checkers(vim.eval('ft'))
cmds = [(c.checker, c.format_cmd(vim.eval('tmp'))) for c in loaded.values()]
EOF

  let cmds = Pyeval('cmds')
  let written = v:false

  for [checker, cmd] in cmds
    if empty(cmd)
      continue
    endif
    if !written
      call writefile(lines, tmp)
      let s:files[tmp] = 1
      let written = v:true
    endif
    let job = job_start(cmd, {"close_cb": {c->s:handle(c, ft, nr, checker)}, "in_io": 'null', "err_io": 'out'})
    call s:manager.add_job(job)
  endfor

  " no job spawned
  if written && s:manager.refcount <= 0
    call s:manager.decref()
  endif
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


function! s:on_vim_leave()
  for f in keys(s:files)
    try | call delete(f) | catch | endtry
  endfor
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
        autocmd VimLeave * call s:on_vim_leave()
    augroup END
endfunction


function! s:define_sign(type, symbol)
  exe 'sign define Validator'.a:type.' text='.a:symbol.' texthl=Validator'.a:type.'Sign'
endfunction


function! s:highlight()
  hi default ValidatorErrorSign ctermfg=88 ctermbg=235
  hi default ValidatorWarningSign ctermfg=3 ctermbg=235
  hi default link ValidatorStyleErrorSign ValidatorErrorSign
  hi default link ValidatorStyleWarningSign ValidatorWarningSign

  call s:define_sign('Error', g:validator_error_symbol)
  call s:define_sign('Warning', g:validator_warning_symbol)
  call s:define_sign('StyleError', g:validator_style_error_symbol)
  call s:define_sign('StyleWarning', g:validator_style_warning_symbol)
endfunction


function! validator#enable()
    if &diff
        return
    endif

    Py import validator, vim

    command! ValidatorCheck call s:check()

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
