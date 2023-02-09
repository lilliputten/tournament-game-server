# -*- coding:utf-8 -*-
# @module logger
# @since 2020.02.23, 02:18
# @changed 2022.02.24, 00:53


import traceback

#  from . import utils
from . import yamlSupport


def toString(error, show_stacktrace=False):
    errorName = type(error).__name__
    errorExtra = str(error)
    #  TODO: Add all args?
    errorArg = str(error.args[0]) if error.args and error.args[0] else ''
    if errorArg and errorArg != errorExtra:
        errorExtra += ' (' + errorArg + ')'
    errorStr = errorName + ': ' + errorExtra
    stack = traceback.format_exc()
    if stack and show_stacktrace:
        errorStr += '\n' + stack
    return errorStr


def toBlockString(error):
    errorStr = toString(error)
    return yamlSupport.BlockString(errorStr)


__all__ = [  # Exporting objects...
    'toString',
    'toBlockString',
]
