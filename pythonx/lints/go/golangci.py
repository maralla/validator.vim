# -*- coding: utf-8 -*-

import logging
import os
from validator import Validator

logger = logging.getLogger('validator')


class Golangci(Validator):
    __filetype__ = 'go'

    instant = False
    checker = 'golangci-lint'
    args = '--out-format line-number'
    regex = r"""
        .+?:
        (?P<lnum>\d+):
        (?P<col>\d+):
        \s
        (?P<text>.*)
    """

    @property
    def cwd(self):
        return os.getcwd()

    def cmd(self, fpath):
        logger.info(fpath)
        return ' '.join([self.binary, "run", self.cmd_args, self.filename])
