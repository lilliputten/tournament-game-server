# -*- coding:utf-8 -*-
# @module utils
# @since 2020.02.23, 02:18
# @changed 2023.02.13, 23:51


import traceback
import re


def empty(var):
    return not var and var is None


def msTimeFromSec(sec):
    return sec * 1000


def msTimeFromMin(min):
    return msTimeFromSec(min * 60)


def quoteStr(s, addQuotes=False, quoteDouble=False, quoteSingle=True):
    """
    s (str) -- Source string parameter.
    Options:
    - addQuotes (bool|str) -- Add quotes around result string (default: False, don't quote).
    - quoteSingle (bool) -- Quote single quotes ('), default is True.
    - quoteDouble (bool) -- Quote double quotes ("), default is False.
    Returns string.
    """
    if not isinstance(s, str):  # type(s) != str:
        if s is None:
            s = ''
        else:
            s = str(s)
    if quoteDouble:
        s = s.replace('"', '\\"')
    if quoteSingle:
        s = s.replace('\'', '\\\'')
    if addQuotes:
        if addQuotes is True:
            addQuotes = "'"
        s = addQuotes + s + addQuotes
    return s


def dictFromClass(cls):
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        #  if key not in _excluded_keys
    )


def truncateLongString(s, maxLength=0):
    if maxLength and len(s) >= maxLength:
        s = s[0:maxLength - 3] + '...'
    return s


def prepareLongString(s, maxLength=0):
    s = re.sub(r'\s+\n', '\n', s)
    return truncateLongString(s, maxLength)


def getTrace(appendStr=None):
    # NOTE: Required to pass extracted traceback
    traces = traceback.extract_stack(None, 2)
    lastTrace = traces[0]
    modPath = lastTrace[0]
    modNameMatch = re.search(r'([^\\/]*).py$', modPath)
    modName = modNameMatch.group(1) if modNameMatch else modPath
    funcName = lastTrace[2]
    strList = [
        '@',
        #  __name__,
        modName,
        funcName,
        appendStr,
    ]
    filteredList = list(filter(None, strList))
    traceResult = ':'.join(filteredList)
    #  print('@:testUtils:getTrace', {
    #      #  'traceResult': traceResult,
    #      #  'traces': traces,
    #      #  'lastTrace': lastTrace,
    #      #  'modPath': modPath,
    #      'modName': modName,
    #      'funcName': funcName,
    #  })
    return traceResult


__all__ = [  # Exporting objects...
    'empty',
    'msTimeFromSec',
    'msTimeFromMin',
    'quoteStr',
    'dictFromClass',
    'truncateLongString',
    'prepareLongString',
    'getTrace',
]
