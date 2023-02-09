# -*- coding:utf-8 -*-
# @module blueprintRequests
# @desc Requests API
# @since 2022.03.25, 18:57
# @changed 2022.04.02, 15:39

import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

from config import config
from src import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getDateStr,
    getMsTimeStamp,
)
#  from src.core.lib import utils
from src.core.lib.utils import getTrace
from src import appSession

from src.core.Requests.RequestsStorageSingleton import requestsStorage

blueprintRequests = Blueprint('blueprintRequests', __name__)

apiRoot = config['apiRoot']
requestsApiRoot = apiRoot + '/requests'

DEBUG('@:blueprintRequests: starting', {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
    'requestsApiRoot': requestsApiRoot,
})


#  # TODO: List requests...
#  @blueprintRequests.route(requestsApiRoot)
#  def blueprintRequests_list():
#      requestError = serverUtils.checkInvalidRequestError()
#      if requestError:
#          return requestError
#      requestsStorage.dbSync()
#      requests = requestsStorage.getAllData()
#      requestsStorage.dbClose()
#      DEBUG(getTrace(), {
#          'requests': requests,
#      })
#      res = jsonify(requests)
#      appSession.addExtendedSessionToResponse(res)
#      return res


@blueprintRequests.route(requestsApiRoot + '/add', methods=['POST'])
def blueprintRequests_add():
    requestError = serverUtils.checkInvalidRequestError(checkToken=True)
    if requestError:
        return requestError
    # Get request data
    requestData = request.json  # request.values
    if requestData is None or not requestData:
        errStr = 'Got empty request data!'
        raise Exception(errStr)
    if 'requestType' not in requestData or not requestData['requestType']:
        errStr = 'Not specified parameter `requestType`!'
        raise Exception(errStr)
    # Get request type
    requestType = requestData['requestType']
    # Prepare extra parameters...
    now = datetime.datetime.now()
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    timestr = getDateStr(now)
    ip = request.remote_addr
    #  hasToken = appSession.hasToken()
    Token = appSession.getOrCreateToken(getTrace())
    extraData = {
        'timestamp': timestamp,
        'timestr': timestr,
        'ip': ip,
        #  'hasToken': hasToken,
        'Token': Token,
    }
    # Combine record data
    data = dict(requestData, **extraData)
    # Add record item...
    requestsStorage.dbSync()
    recordId = requestsStorage.addRecord(timestamp=timestamp, requestType=requestType, data=data)
    requestsStorage.dbClose()
    # Prepare result data...
    resultData = {
        #  'requestData': requestData,
        #  'extraData': extraData,
        'data': data,
        'recordId': recordId,
    }
    DEBUG(getTrace(), resultData)
    # Make result...
    res = jsonify(resultData)
    appSession.addExtendedSessionToResponse(res)
    return res


__all__ = [  # Exporting objects...
    'blueprintRequests',
]

if __name__ == '__main__':
    DEBUG('@:blueprintRequests: debug run')
