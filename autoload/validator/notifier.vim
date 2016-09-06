let s:sign_id = 0
let s:used_sign_ids = {}

function! validator#notifier#notify(loclist, bufnr)
  call s:mark(a:bufnr)
  let g:sign_map[a:bufnr] = {}

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

    if !has_key(s:used_sign_ids, a:bufnr)
      let s:used_sign_ids[a:bufnr] = {}
    endif

    let s:sign_id += 1
    let line = lnum < 1 ? 1 : lnum
    let s:used_sign_ids[a:bufnr][s:sign_id] = v:false

    try
      exec "sign place ".s:sign_id." line=".line." name=".type." buffer=".a:bufnr
    catch
    endtry

    let g:sign_map[a:bufnr][line] = loc['text']
  endfor

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
