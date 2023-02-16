# -*- coding:utf-8 -*-
# @module tinydb utils & helpers
# @since 2023.02.13, 15:00
# @changed 2023.02.13, 15:00

from tinydb import Query
from datetime import datetime

from src.core.lib.logger import (
    getMsTimeStamp,
)

from . import WaitingConstants


def getInvalidRecordQuery(findInvalidRecords=False, Token=None):
    """
    Create tinyDB query for fetching (removing) obsolete records and records
    with current token (if flag `findInvalidRecords` passed).
    """
    timestamp = getMsTimeStamp(datetime.now())  # Get milliseconds timestamp (for technical usage)
    validTimestamp = timestamp - WaitingConstants.validWaitingPeriodMs
    q = Query()
    query = q.timestamp < validTimestamp
    if findInvalidRecords and Token and Token is not None:
        #  Token = appSession.getToken()
        # Remove all records with current token
        query = (q.Token == Token) | query
    return query


def getValidRecordQuery(Token=None):
    """
    Create tinyDB query for fetching (removing) actual records and records
    with current token (if flag `findInvalidRecords` passed).
    """
    timestamp = getMsTimeStamp(datetime.now())  # Get milliseconds timestamp (for technical usage)
    validTimestamp = timestamp - WaitingConstants.validWaitingPeriodMs
    q = Query()
    query = q.timestamp >= validTimestamp
    if Token and Token is not None:
        #  Token = appSession.getToken()
        # Remove all records with current token
        query = (q.Token == Token) & query
    return query


__all__ = [  # Exporting objects...
    'getInvalidRecordQuery',
    'getValidRecordQuery',
]
