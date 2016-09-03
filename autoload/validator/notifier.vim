let s:sign_id = 0
let s:used_sign_ids = {}

function! validator#notifier#notify(loclist, bufnr)
  call s:clear(a:bufnr)
  let g:sign_map[a:bufnr] = {}

  if len(a:loclist) <= 0
    return
  endif

  let seen = {}

  for loc in a:loclist
    let lnum = loc['lnum']
    if lnum <= 0 || has_key(seen, lnum)
      continue
    endif
    let seen[lnum] = v:true

    let severity = loc["type"] == 'W' ? "Warning" : "Error"
    let subtype = get(loc, 'subtype', '')
    let type = 'Validator'.subtype.severity

    let s:sign_id = s:sign_id + 1
    if !has_key(s:used_sign_ids, a:bufnr)
      let s:used_sign_ids[a:bufnr] = []
    endif
    call add(s:used_sign_ids[a:bufnr], s:sign_id)

    let line = lnum < 1 ? 1 : lnum
    try
      exec "sign place ".s:sign_id." line=".line." name=".type." buffer=".a:bufnr
    catch
    endtry
    let g:sign_map[a:bufnr][line] = loc['text']
  endfor
endfunction


function! s:clear(bufnr)
  let ids = get(s:used_sign_ids, a:bufnr, [])
  let idx = 0
  let length = len(ids)

  for i in reverse(copy(ids))
    let idx += 1
    try
      exec "sign unplace ".i." buffer=".a:bufnr
    catch /E158/
    endtry
    call remove(ids, length - idx)
  endfor
endfunction
