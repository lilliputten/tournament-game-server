# -*- coding:utf-8 -*-
# @module blueprintRootApi
# @desc Records API
# @since 2022.03.25, 18:57
# @changed 2022.03.29, 22:46

import datetime

from flask import Blueprint
from flask import jsonify
#  from flask import request
#  from flask import session
#  from flask_cors import cross_origin

from config import config
from src import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    #  getMsDateTag,
    getDateStr,
    getMsTimeStamp,
)
#  from src.core.lib import utils
from src.core.lib.utils import getTrace
from src import appSession

blueprintRootApi = Blueprint('blueprintRootApi', __name__)

apiRoot = config['apiRoot']

DEBUG('@:blueprintRootApi: starting', {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
})


@blueprintRootApi.route(apiRoot + '/start')  # , methods=['GET', 'OPTIONS'])
def blueprintRootApi_start():
    requestError = serverUtils.checkInvalidRequestError(checkToken=False)
    if requestError:
        return requestError
    # Prepare parameters...
    requestData = serverUtils.getRequestData()
    # Check token existed. All previous token chekups must be preformed before `getOrCreateToken` call.
    hasToken = appSession.hasToken()
    # Get exists token (continue session) or create new (start session)
    Token = appSession.getOrCreateToken(getTrace())
    # Create timestamps...
    now = datetime.datetime.now()
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    timestr = getDateStr(now)
    #  timetag = getMsDateTag(now)
    responseData = {
        'resumedSession': hasToken,
        'ip': requestData['ip'],
        'Token': Token,
        'timestamp': timestamp,
        #  'timetag': timetag,
        'timestr': timestr,
    }
    DEBUG(getTrace(), dict(requestData, **{'responseData': responseData}))
    res = jsonify(responseData)
    appSession.addExtendedSessionToResponse(res)
    return res


__all__ = [  # Exporting objects...
    'blueprintRootApi',
]

if __name__ == '__main__':
    DEBUG('@:blueprintRootApi: debug run')
