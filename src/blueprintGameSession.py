# -*- coding:utf-8 -*-
# @module blueprintGameSession
# @desc Waiting for game start API
# @since 2023.02.11, 22:03
# @changed 2023.02.12, 00:50

#  import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

from config import config

from src.core.lib import serverUtils

from src.core.lib.logger import DEBUG
#  from src.core.lib.logger import (
#      getDateStr,
#      getMsTimeStamp,
#  )
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth

#  from src.core.Waiting import waitingStorage, WaitingHelpers
from src.core.Game import gameController

blueprintGameSession = Blueprint('blueprintGameSession', __name__)

apiRoot = config['apiRoot']

DEBUG(getTrace('starting'), {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
})


# Serve blueprint..


@blueprintGameSession.route(apiRoot + '/gameSessionStart', methods=['POST'])
@appAuth.auth.login_required
def blueprintGameSession_gameSessionStart():
    # Start error...
    requestError = serverUtils.checkInvalidRequestError(
        checkToken=True, checkGameToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError

    responseData = gameController.startGameSession()
    DEBUG(getTrace(), responseData)
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintGameSession.route(apiRoot + '/gameSessionStop', methods=['POST'])
@appAuth.auth.login_required
def blueprintGameSession_gameSessionStop():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(
        checkToken=True, checkGameToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError
    responseData = gameController.gameSessionStop()
    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintGameSession.route(apiRoot + '/gameSessionFinished', methods=['POST'])
@appAuth.auth.login_required
def blueprintGameSession_gameSessionFinished():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(
        checkToken=True, checkGameToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError
    responseData = gameController.gameSessionFinished()
    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintGameSession.route(apiRoot + '/gameSessionCheck', methods=['POST'])
@appAuth.auth.login_required
def blueprintGameSession_gameSessionCheck():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(
        checkToken=True, checkGameToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError

    responseData = gameController.doSessionCheck(request)

    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintGameSession.route(apiRoot + '/gameSessionCheckAnswer', methods=['POST'])
@appAuth.auth.login_required
def blueprintGameSession_gameSessionCheckAnswer():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkGameToken=True)
    if requestError:
        return requestError

    responseData = gameController.doCheckAnswer(request)

    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


__all__ = [  # Exporting objects...
    'blueprintGameSession',
]

if __name__ == '__main__':
    DEBUG('@:blueprintGameSession: debug run')
