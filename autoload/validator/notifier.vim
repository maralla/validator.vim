let s:sign_id = 0
let s:used_sign_ids = {}

function! validator#notifier#notify(loclist, bufnr)
  call s:mark(a:bufnr)
  let g:sign_map[a:bufnr] = {}

  let seen = {}
  let lists = []

  for loc in a:loclist
    let lnum = get(loc, 'lnum', 0)
    if lnum <= 0 || has_key(seen, lnum)
      continue
    endif
    let seen[lnum] = v:true

    let severity = get(loc, 'type', '') == 'W' ? "Warning" : "Error"
    let subtype = get(loc, 'subtype', '')
    let type = 'Validator'.subtype.severity

    if !has_key(s:used_sign_ids, a:bufnr)
      let s:used_sign_ids[a:bufnr] = {}
    endif

    let s:sign_id += 1
    let s:used_sign_ids[a:bufnr][s:sign_id] = v:false

    try
      exec "sign place ".s:sign_id." line=".lnum." name=".type." buffer=".a:bufnr
    catch
    endtry

    let g:sign_map[a:bufnr][lnum] = get(loc, 'text', '')
    call add(lists, loc)
  endfor

  call setloclist(0, lists, 'r')
  if g:validator_auto_open_quickfix
    lwindow
    if &ft == 'qf'
      wincmd p
    endif
  endif
  call s:clear(a:bufnr)
endfunction


function! s:mark(bufnr)
  let ids = get(s:used_sign_ids, a:bufnr, {})
  for key in keys(ids)
    let ids[key] = v:true
  endfor
endfunction


function! s:clear(bufnr)
  let ids = get(s:used_sign_ids, a:bufnr, {})

  for key in keys(ids)
    if ids[key]
      try
        exec "sign unplace ".key." buffer=".a:bufnr
      catch /E158/
      endtry
      call remove(ids, key)
    endif
  endfor
endfunction
