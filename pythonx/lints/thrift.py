# -*- coding: utf-8 -*-

from __future__ import absolute_import

from validator import Validator


class Thrift(Validator):
    __filetype__ = 'thrift'

    instant = False
    checker = 'thrift'

    regex = r"""
    \[((?P<warning>WARNING)|(?P<error>ERROR)):.*?:(?P<lnum>\d+)\]\s(?P<text>.*)
    """

    def cmd(self, fname):
        return 'bash -c "thrift -o $(mktemp -d) --gen py {}"'.format(fname)
