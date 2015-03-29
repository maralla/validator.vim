from . import SyntaxChecker


class Thrift(SyntaxChecker):
    __filetype__ = "thrift"
    __subname__ = "thrift"

    checker = "thrift"
    args = "--gen py"
    errorformat = ("%E[ERROR:%f:%l] %.%#,"
                   "%C%m"
                   )
