# -*- coding:utf-8 -*-
# @module blueprintWaiting
# @desc Waiting for game start API
# @since 2023.02.11, 22:03
# @changed 2023.02.12, 00:50

import time
from flask import Blueprint
from flask import jsonify
from flask import request

from config import config

from src import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth

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
    appSession.set('name', name)
    # Return success result...
    responseData = {
        'Token': appSession.getToken(),
        'success': True,
        # error
    }
    DEBUG(getTrace(), {'info': 'start waiting'})
    # DEBUG: Emulate loooong request
    time.sleep(5)
    DEBUG(getTrace(), dict(requestData, **{'responseData': responseData}))
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


__all__ = [  # Exporting objects...
    'blueprintWaiting',
]

if __name__ == '__main__':
    DEBUG('@:blueprintWaiting: debug run')
