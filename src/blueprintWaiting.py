# -*- coding:utf-8 -*-
# @module blueprintWaiting
# @desc Waiting for game start API
# @since 2023.02.11, 22:03
# @changed 2023.02.11, 22:29

#  import re

from flask import Blueprint
#  from flask import send_from_directory  # For htmlAppBuild serving
from flask import render_template  # Used for `blueprintWaiting_root_hello`
#  from flask import redirect
from flask import jsonify
from flask import request
#  from flask_cors import cross_origin

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
def blueprintRootApi_setName():
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
    DEBUG(getTrace(), dict(requestData, **{'responseData': responseData}))
    res = jsonify(responseData)
    return appSession.addExtendedSessionToResponse(res)


@blueprintWaiting.route('/')
def blueprintWaiting_root_error():
    DEBUG(getTrace())
    # Emulate error response
    err = {
        #  'code': 400,
        #  'error': 'Bad Request',
    }
    return serverUtils.makeErrorForRequest(err)


@blueprintWaiting.route('/hello')
def blueprintWaiting_root_hello():
    """
    render_template demo
    """
    DEBUG(getTrace())
    return render_template('hello.html')


#  @blueprintWaiting.route('/')
#  @blueprintWaiting.route('/<path:path>')
#  def blueprintWaiting_root_htmlAppBuild(path=None):
#      """
#      Serve static spa app code (prebuilt from `march-team-nextjs-app` project
#      and provided as link with scripts `utils/make-html-app-links.sh`,
#      `utils/make-html-app-links-local.sh`).
#      Too slow and buggy. May be used for rare-used backend app.
#      """
#      htmlAppBuild = config['htmlAppBuild']
#      origPath = path  # Debug only!
#      # Convert page names (without paths) to html file names...
#      if not path or path == '' or path == '/':
#          path = 'index.html'
#      elif re.match(r'^[^/.]*$', path):
#          path += '.html'
#      DEBUG(getTrace(), {
#          'htmlAppBuild': htmlAppBuild,
#          'origPath': origPath,
#          'path': path,
#      })
#      return send_from_directory(htmlAppBuild, path)


__all__ = [  # Exporting objects...
    'blueprintWaiting',
]

if __name__ == '__main__':
    DEBUG('@:blueprintWaiting: debug run')
