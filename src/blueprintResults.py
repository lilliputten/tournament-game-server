# -*- coding:utf-8 -*-
# @module blueprintResults
# @since 2023.03.05, 04:05
# @changed 2023.03.05, 04:10


from flask import Blueprint
from flask import jsonify

from config import config

from src.core.Records import recordsController

from src.core.lib import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth


blueprintResults = Blueprint('blueprintResults', __name__)

apiRoot = config['apiRoot']

DEBUG(getTrace('starting'), {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
})


# Serve blueprint..


@blueprintResults.route(apiRoot + '/loadResults', methods=['GET'])
@appAuth.auth.login_required
def blueprintResults_loadResults():
    """
    loadResults -- Get game records table
    """
    # Start error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True)
    if requestError:
        return requestError

    records = recordsController.getRecentRecords()
    responseData = {
        'success': True,
        # reason
        'results': records,
    }
    DEBUG(getTrace(), responseData)
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


__all__ = [  # Exporting objects...
    'blueprintResults',
]

if __name__ == '__main__':
    DEBUG('@:blueprintResults: debug run')
