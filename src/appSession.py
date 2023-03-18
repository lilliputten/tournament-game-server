# -*- coding:utf-8 -*-
# @module appSession
# @since 2022.02.07, 00:27
# @changed 2023.02.13, 23:26

import datetime

from flask import session
from flask import request

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getMsDateTag,
    getMsTimeStamp,
)
from src.core.lib.uniqueToken import createUniqueToken

from src.core.lib.utils import getTrace

isDev = config['isDev']
useTimeStampInLastAccess = not isDev


def getGameToken():
    return session.get('gameToken')


def hasGameToken():
    return bool(getGameToken())


def hasValidGameToken():
    sessionGameToken = session.get('gameToken')
    cookies = request.cookies
    cookieGameToken = cookies.get('gameToken')
    DEBUG(getTrace(), {
        'sessionGameToken': sessionGameToken,
        'cookieGameToken': cookieGameToken,
        #  'cookies': cookies,
    })
    if sessionGameToken is None or not sessionGameToken:
        return False
    if cookieGameToken is None or not cookieGameToken:
        return False
    if sessionGameToken != cookieGameToken:
        return False
    return True


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
        # Create random token id...
        Token = createUniqueToken()
        DEBUG(getTrace('new session id'), {
            'callerId': callerId,
            'Token': Token,
        })
        session['Token'] = Token
        session['sessionNew'] = True
    else:
        DEBUG('@:appSession:getOrCreateToken: using exists session id', {
            'callerId': callerId,
            'Token': Token,
        })
        session['sessionNew'] = False
    sessionLastAccess = (str(timestamp) + ' ' if useTimeStampInLastAccess else '') + dateTag
    session['sessionLastAccess'] = sessionLastAccess
    return Token


def addExtendedSessionToResponse(res):
    # TODO: Check for regular response?
    Token = session.get('Token', '')  # getOrCreateToken('addExtendedSessionToResponse')
    if Token:
        # TODO: Set samesite in dependency with response origin property?
        res.set_cookie('Token', Token, samesite='None', secure=True)
    gameToken = session.get('gameToken', '')  # getOrCreateToken('addExtendedSessionToResponse')
    if gameToken:
        # TODO: Set samesite in dependency with response origin property?
        res.set_cookie('gameToken', gameToken, samesite='None', secure=True)
    return res


def setVariable(key, value):
    session[key] = value


def getVariable(key, defaultValue=None):
    return session[key] if key in session else defaultValue


def removeVariable(key):
    session.pop(key, default=None)


__all__ = [  # Exporting objects...
    #  'session',
    'getToken',
    'hasToken',
    'hasValidToken',
    'getOrCreateToken',
    'addExtendedSessionToResponse',
    'setVariable',
    'getVariable',
    'removeVariable',
]

if __name__ == '__main__':
    print(getTrace('debug run'))
