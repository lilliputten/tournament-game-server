# -*- coding:utf-8 -*-
# @module blueprintWaiting
# @desc Waiting for game start API
# @since 2023.02.11, 22:03
# @changed 2023.02.12, 00:50

import datetime
# import time

from flask import Blueprint
from flask import jsonify
from flask import request

from tinydb import Query

from config import config

from src import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getDateStr,
    getMsTimeStamp,
)
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth

from src.core.Waiting import waitingStorage, WaitingConstants

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
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkRequestJsonData=True)
    if requestError:
        return requestError
    # Get request data...
    requestData = request.json
    # Get name & store it to session...
    if not requestData or 'name' not in requestData or not requestData['name']:
        errStr = 'Not specified parameter `name`!'
        raise Exception(errStr)
    name = requestData['name']
    appSession.setVariable('name', name)
    # Prepare extra parameters...
    now = datetime.datetime.now()
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    timestr = getDateStr(now)
    ip = request.remote_addr
    #  hasToken = appSession.hasToken()
    Token = appSession.getOrCreateToken(getTrace())
    data = {
        'name': name,
        'timestamp': timestamp,
        'timestr': timestr,
        'ip': ip,
        #  'Token': Token,
        'pairedToken': None,
    }
    # Add record item...
    waitingStorage.dbSync()
    # Create db query...
    validTimestamp = timestamp - WaitingConstants.validWaitingPeriodMs
    q = Query()
    timeQuery = q.timestamp < validTimestamp  # Remove all obsolete records
    tokenQuery = q.Token == Token  # Remo all other records for this token
    comboQuery = tokenQuery | timeQuery
    # Remove all obsolete records...
    removedRecords = waitingStorage.removeRecords(comboQuery)
    # Add updated record
    recordId = waitingStorage.addRecord(
        timestamp=timestamp,
        Token=Token,
        data=data,
    )
    # TODO: Check result of db operation?
    waitingStorage.dbClose()
    # Return success result...
    responseData = dict(data, **{
        'success': True,
        'recordId': recordId,
        # error?
    })
    #  # DEBUG: Emulate loooong request
    #  DEBUG(getTrace(), {'info': 'start waiting'})
    #  time.sleep(5)
    DEBUG(getTrace(), {
        'requestData': requestData,
        'responseData': responseData,
        #  'removedRecords': removedRecords,
        'removedRecordsCount': len(removedRecords),
    })
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintWaiting.route(apiRoot + '/waitingStop', methods=['POST'])
@appAuth.auth.login_required
def blueprintWaiting_waitingStop():
    # Check error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True, checkRequestJsonData=False)
    if requestError:
        return requestError
    Token = appSession.getToken()
    # Add record item...
    waitingStorage.dbSync()
    # Create db query...
    timestamp = getMsTimeStamp(datetime.datetime.now())  # Get milliseconds timestamp (for technical usage)
    validTimestamp = timestamp - WaitingConstants.validWaitingPeriodMs
    q = Query()
    timeQuery = q.timestamp < validTimestamp  # Remove all obsolete records
    tokenQuery = q.Token == Token  # Remo all other records for this token
    comboQuery = tokenQuery | timeQuery
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
