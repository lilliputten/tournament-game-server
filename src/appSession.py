# -*- coding:utf-8 -*-
# @module appSession
# @since 2022.02.07, 00:27
# @changed 2022.04.02, 15:44

import uuid
import random
import datetime

from flask import session
from flask import request

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getMsDateTag,
    getMsTimeStamp,
)

from src.core.lib.utils import getTrace

#  from src.core import RecordsStorage

isDev = config['isDev']
useTimeStampInLastAccess = not isDev
useSimplifiedSessionId = isDev


def getToken():
    return session.get('Token')


def hasToken():
    return bool(getToken())


def hasValidToken():
    sessionToken = session.get('Token')
    cookies = request.cookies
    cookieToken = cookies.get('Token')
    DEBUG(getTrace(), {
        'sessionToken': sessionToken,
        'cookieToken': cookieToken,
        #  'cookies': cookies,
    })
    if sessionToken is None or not sessionToken:
        return False
    if cookieToken is None or not cookieToken:
        return False
    if sessionToken != cookieToken:
        return False
    return True


def getOrCreateToken(callerId=''):
    """
    Get exists token (continue session) or create new (start session).
    All previous token chekups must be preformed before `getOrCreateToken` call
    """
    Token = session.get('Token')
    now = datetime.datetime.now()  # Get current date object
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    dateTag = getMsDateTag(now)
    if not Token:
        # Create random token id (simple for dev mode or uuid for production)
        sesseionIdValue = random.randint(100000, 10000000) if useSimplifiedSessionId else uuid.uuid4()
        # Compose token value using date tag and unique id; TODO: Use PyJWT encoding?
        Token = dateTag + '-' + str(sesseionIdValue)
        DEBUG(getTrace('new session id'), {
            'callerId': callerId,
            'Token': Token,
            #  'sessionIdObj': sessionIdObj,
        })
        session['Token'] = Token
        session['sessionNew'] = True
    else:
        DEBUG('@:appSession:getOrCreateToken: using exists session id', {
            'callerId': callerId,
            'Token': Token,
        })
        session['sessionNew'] = False
    #  sessionLastAccess = str(timestamp) + ' ' + dateTag
    sessionLastAccess = (str(timestamp) + ' ' if useTimeStampInLastAccess else '') + dateTag
    session['sessionLastAccess'] = sessionLastAccess
    return Token


def addExtendedSessionToResponse(res):
    Token = session.get('Token', '')  # getOrCreateToken('addExtendedSessionToResponse')
    if Token:
        res.set_cookie('Token', Token, samesite='None', secure=True)


__all__ = [  # Exporting objects...
    #  'session',
    'getToken',
    'hasToken',
    'hasValidToken',
    'getOrCreateToken',
    'addExtendedSessionToResponse',
]

if __name__ == '__main__':
    print(getTrace('debug run'))
