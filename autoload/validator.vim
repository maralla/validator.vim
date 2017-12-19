" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:loclist = []
let s:tempfile = tempname()
let s:width = 16
let s:python_imported = v:false
let s:events = {}

let s:manager = {'refcount': 0, 'jobs': []}


function! s:manager.add_job(job)
  if job_status(a:job) == 'run'
    call add(self.jobs, a:job)
    let self.refcount += 1
  endif
endfunction

function! s:manager.reset_jobs()
  let still_alive = []
  for job in self.jobs
    if job_status(job) == 'run'
      call job_stop(job)
      " recheck
      if job_status(job) == 'run'
        call add(still_alive, job)
      else
        call self.decref()
      endif
    endif
  endfor
  let self.jobs = still_alive
endfunction

function! s:manager.decref()
  let self.refcount -= 1
  if self.refcount <= 0
    let self.refcount = 0
  endif
endfunction


function! s:handle(ch, ft, nr, checker)
  call s:manager.decref()

  let msg = []
  while ch_status(a:ch) == 'buffered'
    call add(msg, ch_read(a:ch))
  endwhile

  if !bufexists(a:nr) | return | endif

  let s:loclist += validator#utils#parse_loclist(msg, a:nr, a:ft, a:checker)
  if s:manager.refcount <= 0
    call validator#notifier#notify(s:loclist, a:nr)
    let s:loclist = []
  endif
endfunction


function! s:clear(nr)
  let s:loclist = []
  if has_key(g:_validator_sign_map, a:nr)
    call validator#notifier#notify(s:loclist, a:nr)
  endif
endfunction


function! s:send_buffer(job, lines)
  let ch = job_getchannel(a:job)
  if ch_status(ch) == 'open'
    call ch_sendraw(ch, join(a:lines, "\n"))
    call ch_close_in(ch)
  endif
endfunction


function! s:import_python()
  if !s:python_imported
    call validator#utils#setup_python()
    let s:python_imported = v:true
  endif
endfunction


function! s:check(instant)
  call s:import_python()

  let ft = &filetype
  if  pumvisible() || index(g:validator_ignore, ft) != -1 | return | endif

  let nr = bufnr('')
  if empty(ft)
    call s:clear(nr)
    return
  endif

  call s:manager.reset_jobs()

  let ext = expand('%:e')
  let ext = empty(ext) ? '' : '.'.ext
  let tail = fnamemodify(s:tempfile, ':t')
  let fname = 'temp'.tail.ext
  let tmp = fnamemodify(s:tempfile, ':s?'.tail.'$?'.fname.'?')

  let lines = getline(1, '$')
  if len(lines) == 1 && empty(lines[0])
    call s:clear(nr)
    return
  endif

  let cmds = validator#utils#load_checkers(ft, tmp, a:instant)
  let written = v:false

  for cmd_spec in cmds
    if empty(cmd_spec.cmd) | continue | endif
    if !cmd_spec.stdin && !written
      call writefile(lines, tmp)
      let written = v:true
    endif
    let options = {
          \ "close_cb": s:gen_handler(ft, nr, cmd_spec.checker),
          \ "in_io": cmd_spec.stdin ? 'pipe' : 'null',
          \ "err_io": 'out',
          \ "stoponexit": ""
          \ }
    if !empty(cmd_spec.cwd)
      let options.cwd = cmd_spec.cwd
    endif
    let job = job_start(cmd_spec.cmd, options)
    if cmd_spec.stdin
      call s:send_buffer(job, lines)
    endif
    call s:manager.add_job(job)
  endfor
endfunction


function! s:gen_handler(ft, nr, checker)
  return {c->s:handle(c, a:ft, a:nr, a:checker)}
endfunction


function! s:on_cursor_move()
  let nr = bufnr('')
  let line = line('.')

  if !has_key(g:_validator_sign_map, nr)
    return
  endif

  let info = get(get(g:_validator_sign_map[nr], 'text', {}), line, {})
  let msg = get(info, 'msg', '')
  let hi_type = get(info, 'type', 'NONE')
  let expected = &columns - s:width
  if strwidth(msg) > expected
    let msg = msg[:expected].'...'
  endif
  if g:validator_highlight_message
    exe 'echohl ' . hi_type
  endif
  echo msg
  if g:validator_highlight_message
    echohl NONE
  endif
endfunction


function! s:do_check()
  let instant = has_key(s:events, 'text_changed') || has_key(s:events, 'text_changed_i')
  try
    if !empty(s:events)
      call s:check(instant)
    endif
  finally
    let s:events = {}
  endtry
endfunction


function! s:add_task(event)
  let s:events[a:event] = v:true
  if !exists('s:timer') || empty(timer_info(s:timer))
    let s:timer = timer_start(800, {t->s:do_check()})
  endif
endfunction


function! validator#enable_events()
  augroup validator
    autocmd!
    autocmd CursorMoved  * call s:on_cursor_move()
    autocmd TextChangedI * call s:add_task('text_changed_i')
    autocmd TextChanged  * call s:add_task('text_changed')
    autocmd BufReadPost  * call s:add_task('read_post')
    autocmd BufWritePost * call s:add_task('write_post')
  augroup END
endfunction


function! validator#disable_events()
  augroup validator
    autocmd!
  augroup END
endfunction


function! s:define_sign(type, symbol)
  exe 'sign define Validator'.a:type.' text='.a:symbol.' texthl=Validator'.a:type.'Sign'
endfunction


function! s:highlight()
  hi default link ValidatorErrorSign Error
  hi default link ValidatorWarningSign Exception
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

    command! ValidatorCheck call s:check()

    call s:highlight()
    call validator#enable_events()

    if g:validator_permament_sign
      autocmd BufEnter * exec 'sign define ValidatorEmpty'
      autocmd BufEnter * exec 'exe ":sign place 9999 line=1 name=ValidatorEmpty buffer=".bufnr("")'
    endif
    call s:add_task('init')
endfunction


function! validator#disable()
  call validator#disable_events()
  call validator#notifier#clear()
endfunction


function! validator#get_status_string()
  let nr = bufnr('')
  let text_map = get(get(g:_validator_sign_map, nr, {}), 'text', {})
  let signs = sort(map(keys(text_map), {i,x->str2nr(x)}), {a,b->a==b?0:a>b?1:-1})
  return empty(signs) ? '' : printf(g:validator_error_msg_format, signs[0], len(signs))
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
