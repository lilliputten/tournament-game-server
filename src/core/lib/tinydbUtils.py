# -*- coding:utf-8 -*-
# @module tinydb utils & helpers
# @since 2023.02.12, 16:09
# @changed 2023.02.12, 17:00


def isDbOpened(db):
    """
    Check db is opened
    """
    if db is not None and db._opened:
        return True
    return False


def isQuery(obj):
    """
    Check object is instance of QueryImpl
    """
    objStr = str(obj)
    if objStr.startswith('QueryImpl('):
        return True
    return False


__all__ = [  # Exporting objects...
    'isQuery',
]
