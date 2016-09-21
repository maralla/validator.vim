Validator
=========

Syntax check framework for vim which checks syntax on the fly asynchronously.


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
* javascript, `jshint`, `eslint`
* json, `jsonlint`


Configuration
-------------

Select checkers for a file type:

```vim
let g:validator_{filetype}_checkers = ['<checker_name>']

" for example, choose eslint to check javascript:
let g:validator_javascript_checkers = ['eslint']
```

You can customize error message:

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


Install
-------

I recommend to use a plugin manager for installing.

If you use [vim-plug](https://github.com/junegunn/vim-plug)

    Plug 'maralla/validator.vim'
