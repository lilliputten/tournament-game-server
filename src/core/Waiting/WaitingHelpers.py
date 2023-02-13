# -*- coding:utf-8 -*-
# @module tinydb utils & helpers
# @since 2023.02.13, 15:00
# @changed 2023.02.13, 15:00

from tinydb import Query
import datetime

from src.core.lib.logger import (
    getMsTimeStamp,
)

from . import WaitingConstants


def getValidRecordQuery(removeCurrentTokenRecords=False, validPeriodMs=0, Token=None):
    """
    Create tinyDB query for fetching (removing) obsolete records and records
    with current token (if flag `removeCurrentTokenRecords` passed).
    """
    timestamp = getMsTimeStamp(datetime.datetime.now())  # Get milliseconds timestamp (for technical usage)
    validTimestamp = timestamp - WaitingConstants.validWaitingPeriodMs
    q = Query()
    query = q.timestamp < validTimestamp  # Remove all obsolete records
    if removeCurrentTokenRecords and Token and Token is not None:
        #  Token = appSession.getToken()
        # Remove all records with current token
        query = (q.Token == Token) | query
    return query


__all__ = [  # Exporting objects...
    'getValidRecordQuery',
]
