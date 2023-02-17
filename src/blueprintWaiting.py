# -*- coding:utf-8 -*-
# @module blueprintWaiting
# @desc Waiting for game start API
# @since 2023.02.11, 22:03
# @changed 2023.02.14, 21:04

# from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request
# from tinydb import Query
# from tinydb.table import Document

from config import config

from src.core.lib import serverUtils

from src.core.lib.logger import DEBUG
# from src.core.lib.logger import (
#     getDateStr,
#     getMsTimeStamp,
# )
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth

from src.core.Waiting import waitingStorage, WaitingHelpers
from src.core.Game import gameController

blueprintWaiting = Blueprint('blueprintWaiting', __name__)

apiRoot = config['apiRoot']

DEBUG(getTrace('starting'), {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
})


# Serve blueprint..


@blueprintWaiting.route(apiRoot + '/waitingStart', methods=['POST'])
@appAuth.auth.login_required
def blueprintWaiting_waitingStart():
    # appSession.removeVariable('gameToken')
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkRequestJsonData=True)
    if requestError:
        return requestError

    responseData = gameController.doWaitingStart(request)

    #  # DEBUG: Emulate loooong request
    #  DEBUG(getTrace(), {'info': 'start waiting'})
    #  time.sleep(5)

    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintWaiting.route(apiRoot + '/waitingCheck', methods=['POST'])
@appAuth.auth.login_required
def blueprintWaiting_waitingCheck():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError
    # Try start game session...
    # Token = appSession.getToken()
    responseData = gameController.doWaitingCheck()
    DEBUG(getTrace(), {
        'responseData': responseData,
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintWaiting.route(apiRoot + '/waitingStop', methods=['POST'])
@appAuth.auth.login_required
def blueprintWaiting_waitingStop():
    appSession.removeVariable('gameToken')
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError
    # Add record item...
    waitingStorage.dbSync()
    # Create db query...
    Token = appSession.getToken()
    comboQuery = WaitingHelpers.getInvalidRecordQuery(findInvalidRecords=True, Token=Token)
    # Remove all obsolete records and records with current token...
    removedRecords = waitingStorage.removeRecords(comboQuery)
    # TODO: Check result of db operation?
    waitingStorage.dbClose()
    # Return success result...
    responseData = {
        'success': True,
        # error?
    }
    DEBUG(getTrace(), {
        'responseData': responseData,
        #  'removedRecords': removedRecords,
        'removedRecordsCount': len(removedRecords),
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


__all__ = [  # Exporting objects...
    'blueprintWaiting',
]

if __name__ == '__main__':
    DEBUG('@:blueprintWaiting: debug run')
