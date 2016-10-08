let s:sign_id = 0

function! validator#notifier#notify(loclist, bufnr)
  if !has_key(g:_sign_map, a:bufnr)
    let g:_sign_map[a:bufnr] = {}
  endif

  let ids = get(g:_sign_map[a:bufnr], 'id', [])
  let g:_sign_map[a:bufnr] = {'text': {}, 'id': []}

  let seen = {}
  let lists = []

  for loc in a:loclist
    let lnum = get(loc, 'lnum', 0)
    if lnum <= 0 || has_key(seen, lnum)
      continue
    endif
    let seen[lnum] = v:true

    let severity = get(loc, 'type', '') ==? 'W' ? 'Warning' : 'Error'
    let subtype = get(loc, 'subtype', '')
    let type = 'Validator'.subtype.severity

    let s:sign_id += 1
    call add(g:_sign_map[a:bufnr]['id'], s:sign_id)
    let g:_sign_map[a:bufnr]['text'][lnum] = get(loc, 'text', '')
    call add(lists, loc)

    try
      exec 'sign place '.s:sign_id.' line='.lnum.' name='.type.' buffer='.a:bufnr
    catch
    endtry
  endfor

  call setloclist(0, lists, 'r')
  if g:validator_auto_open_quickfix
    lwindow
    if &ft ==? 'qf'
      wincmd p
    endif
  endif
  call s:clear(a:bufnr, ids)
endfunction


function! s:clear(bufnr, ids)
  for id in a:ids
    try
      exec 'sign unplace '.id.' buffer='.a:bufnr
    catch /E158/
    endtry
  endfor
endfunction
