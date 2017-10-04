" vim: et ts=2 sts=2 sw=2

let s:save_cpo = &cpo
set cpo&vim

let s:loclist = []
let s:tempfile = tempname()
let s:width = 16

let s:manager = {'refcount': 0, 'jobs': []}

function s:manager.add_job(job)
  if job_status(a:job) == 'run'
    call add(self.jobs, a:job)
    let self.refcount += 1
  endif
endfunction

function s:manager.reset_jobs()
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

function s:manager.decref()
  let self.refcount -= 1
  if self.refcount <= 0
    let self.refcount = 0
  endif
endfunction


function s:handle(ch, ft, nr, checker)
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
  if has_key(g:_sign_map, a:nr)
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


function! s:check()
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
  echo tmp

  let lines = getline(1, '$')
  if len(lines) == 1 && empty(lines[0])
    call s:clear(nr)
    return
  endif

  let cmds = validator#utils#load_checkers(ft, tmp)
  let written = v:false

  for [checker, cmd, stdin] in cmds
    if empty(cmd) | continue | endif
    if !stdin && !written
      call writefile(lines, tmp)
      let written = v:true
    endif
    let in_io = stdin ? 'pipe' : 'null'
    let job = job_start(cmd, {"close_cb": s:gen_handler(ft, nr, checker), "in_io": in_io, "err_io": 'out', "stoponexit": ""})
    if stdin
      call s:send_buffer(job, lines)
    endif
    call s:manager.add_job(job)
  endfor
endfunction


function s:gen_handler(ft, nr, checker)
  return {c->s:handle(c, a:ft, a:nr, a:checker)}
endfunction


function! s:on_cursor_move()
  let nr = bufnr('')
  let line = line('.')

  if !has_key(g:_sign_map, nr)
    return
  endif

  let msg = get(get(g:_sign_map[nr], 'text', {}), line, '')
  let expected = &columns - s:width
  if strwidth(msg) > expected
    let msg = msg[:expected].'...'
  endif
  echo msg
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

    call validator#utils#setup_python()

    command! ValidatorCheck call s:check()

    call s:highlight()
    call s:install_event_handlers()

    if g:validator_permament_sign
      autocmd BufEnter * exec 'sign define ValidatorEmpty'
      autocmd BufEnter * exec 'exe ":sign place 9999 line=1 name=ValidatorEmpty buffer=".bufnr("")'
    endif

    call s:check()
endfunction


function! validator#get_status_string()
  let nr = bufnr('')
  let text_map = get(get(g:_sign_map, nr, {}), 'text', {})
  let signs = sort(map(keys(text_map), {i,x->str2nr(x)}), {a,b->a==b?0:a>b?1:-1})
  return empty(signs) ? '' : printf(g:validator_error_msg_format, signs[0], len(signs))
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
