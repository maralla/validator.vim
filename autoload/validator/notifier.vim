let s:sign_id = 0x1000


function! s:pop_id(bufnr)
  if !has_key(g:_validator_sign_map, a:bufnr)
    let g:_validator_sign_map[a:bufnr] = {'text': {}, 'id': []}
  endif

  let ids = g:_validator_sign_map[a:bufnr].id
  let g:_validator_sign_map[a:bufnr].text = {}
  let g:_validator_sign_map[a:bufnr].id = []
  return ids
endfunction


function! s:hl_position(lnum, col)
  return matchadd('ValidatorPosition', '\%'.a:lnum.'l\%'.a:col.'v')
endfunction


function! validator#notifier#notify(loclist, bufnr)
  let ids = s:pop_id(a:bufnr)

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
    let msg = get(loc, 'text', '')
    let col = get(loc, 'col', -1)
    let type = 'Validator'.subtype.severity

    let s:sign_id += 1
    let hl_id = col != -1 ? s:hl_position(lnum, col) : -1
    call add(g:_validator_sign_map[a:bufnr].id, [s:sign_id, hl_id])
    let g:_validator_sign_map[a:bufnr].text[lnum] = {'msg': msg, 'type': type.'Sign'}
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
  for [id, hl_id] in a:ids
    try
      exec 'sign unplace '.id.' buffer='.a:bufnr
    catch /E158/
    endtry
    if hl_id != -1
      call matchdelete(hl_id)
    endif
  endfor
endfunction


function! validator#notifier#clear()
  let buflist = getbufinfo()
  for buf in buflist
    let ids = s:pop_id(buf.bufnr)
    call s:clear(buf.bufnr, ids)
  endfor
endfunction
