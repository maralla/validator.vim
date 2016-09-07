Validator
=========

Syntax check framework for vim which checks syntax on the fly asynchronously.


Requirements
------------

You should have a relatively new version of vim which supports such features:
`job`, `timer` and `lambda`.

Your vim should be compiled with `python` or `python3`.

Validator relies on external syntax checkers, so you need to install the checkers
fit for the files you are editting.


Builtin Checkers
----------------

* python, `flake8`
* cython, `cython`
* css, `csslint`
* javascript, `jshint`


Install
-------

I recommend to use a plugin manager for installing.

If you use [vim-plug](https://github.com/junegunn/vim-plug)

    Plug 'maralla/validator.vim'
