# -*- coding:utf-8 -*-
# @module blueprintQuestions
# @since 2023.02.11, 22:03
# @changed 2023.02.16, 01:06

#  import datetime

from flask import Blueprint
from flask import jsonify

from config import config
from src.core.Questions import questions

from src.core.lib import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
from src import appSession
from src import appAuth


blueprintQuestions = Blueprint('blueprintQuestions', __name__)

apiRoot = config['apiRoot']

DEBUG(getTrace('starting'), {
    'buildTag': config['buildTag'],
    'apiRoot': apiRoot,
})


# Serve blueprint..


@blueprintQuestions.route(apiRoot + '/loadQuestions', methods=['GET'])
@appAuth.auth.login_required
def blueprintQuestions_loadQuestions():
    """
    loadQuestions
    """
    # Start error...
    requestError = serverUtils.checkInvalidRequestError(checkToken=True)
    if requestError:
        return requestError

    data = questions.getClientQuestionsData()
    responseData = dict(data, **{
        'success': True,
    })
    DEBUG(getTrace(), responseData)
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


__all__ = [  # Exporting objects...
    'blueprintQuestions',
]

if __name__ == '__main__':
    DEBUG('@:blueprintQuestions: debug run')
