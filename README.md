Validator
=========

[![Build Status](https://travis-ci.org/maralla/validator.vim.svg?branch=master)](https://travis-ci.org/maralla/validator.vim)

Syntax check framework for vim which checks syntax on the fly asynchronously.

<img src="https://i.imgur.com/L8eu6Zb.gif" width="684" height="482">

Requirements
------------

You should have a relatively new version of vim which supports such features:
`job`, `timers` and `lambda`.

Your vim should be compiled with `python` or `python3`.

Validator relies on external syntax checkers, so you need to install the checkers
fit for the files you are editting.

Builtin Checkers
----------------

* c/c++, `clang-tidy`
* python, `flake8`
* cython, `cython`
* css, `csslint`
* javascript, `jshint`, `eslint`, `jscs`
* ruby, `mri`, `rubocop`
* json, `jsonlint`
* lua, `luac`, `luacheck`
* sh, `sh`, `shellcheck`
* rst, `rst2pseudoxml`
* vim, `vint`, `vimlparser`
* go, `gofmt`, `golint`, `gometalinter`
* rust, `cargo check` (not instant)

Configuration
-------------

Select checkers for a file type:

```vim
let g:validator_{filetype}_checkers = ['<checker_name>']

" for example, choose eslint to check javascript:
let g:validator_javascript_checkers = ['eslint']
```

To customize error message:

```vim
let g:validator_error_msg_format = "[ ● %d/%d issues ]"
```

To auto open quickfix window:

```vim
let g:validator_auto_open_quickfix = 1
```

To handle file type alias:

```vim
let g:validator_filetype_map = {'<alias>': '<filetype_supported>'}

" for example
let g:validator_filetype_map = {"python.django": "python"}
```

Ignore file types:

```vim
let g:validator_ignore = ['<filetype>']
```

To customize the signs colors, you can use the following groups:

```vim
" For syntax errors & warnings
ValidatorErrorSign
ValidatorWarningSign

" For style errors & warnings
" (By default, use the same colors as the 2 groups above)
ValidatorStyleErrorSign
ValidatorStyleWarningSign
```

To show permanently the sign column and prevent annonying behavior when the
sign column appear and then it disappears.

![sign](https://i.imgur.com/nGXEijq.jpg)

```vim
let g:validator_permament_sign = 1
```

To specify the checker executable path or pass checker arguments manually:

```vim
" If not specified `<args_name>` is `<filetype>_<checker>`.
let g:validator_<args_name>_args = '<args>'
" If not specified `<binary_name>` is `<filetype>_<checker>`.
let g:validator_<binary_name>_binary = '/path/to/executable'

" For c/c++
let g:validator_clang_tidy_binary = '/path/to/executable'

" For flake8
let g:validator_python_flake8_args = '--max-line-length=120'
let g:validator_python_flake8_binary = '/Users/maralla/.dotfiles/virtualenvs/py27/bin/flake8'

" For rubocop
let g:validator_ruby_rubocop_args = '-f s -c .rubocop.yml'
let g:validator_ruby_rubocop_binary = '/Users/maralla/.rvm/gems/ruby-2.3.0/bin/rubocop'
```

Install
-------

* [pack](https://github.com/maralla/pack)

```bash
$ pack install maralla/validator.vim
```

* [vim-plug](https://github.com/junegunn/vim-plug)

```vim
Plug 'maralla/validator.vim'
```

Usage
-----

Validator.vim automatically checks syntax in the background when file content
changes, so no need to do any trigger manually. If you do want to do a check
manually use this command `ValidatorCheck`. This command is especially useful
when you set the file type manually.

Debugging
-----

Enable the debugging with:

```vim
let g:validator_debug = 1
```

The output is logged in plugin installation directory:

e.g.  `/path/to/validator.vim/pythonx/validator.log`
