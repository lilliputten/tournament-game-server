# -*- coding:utf-8 -*-
# @module blueprintCoreSite
# @desc Records API
# @since 2022.03.27, 20:37
# @changed 2022.04.02, 14:49

#  import re

from flask import Blueprint
#  from flask import send_from_directory  # For htmlAppBuild serving
from flask import render_template  # Used for `blueprintCoreSite_root_hello`
#  from flask import redirect
#  from flask import jsonify
#  from flask import request
#  from flask_cors import cross_origin

from config import config

from src import serverUtils

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
#  from src import appSession

blueprintCoreSite = Blueprint('blueprintCoreSite', __name__)

DEBUG(getTrace('starting'), {
    'buildTag': config['buildTag'],
})


# Serve app..


@blueprintCoreSite.route('/')
def blueprintCoreSite_root_error():
    DEBUG(getTrace())
    # Emulate error response
    err = {
        #  'code': 400,
        #  'error': 'Bad Request',
    }
    return serverUtils.makeErrorForRequest(err)


@blueprintCoreSite.route('/hello')
def blueprintCoreSite_root_hello():
    """
    render_template demo
    """
    DEBUG(getTrace())
    return render_template('hello.html')


#  @blueprintCoreSite.route('/')
#  @blueprintCoreSite.route('/<path:path>')
#  def blueprintCoreSite_root_htmlAppBuild(path=None):
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
    'blueprintCoreSite',
]

if __name__ == '__main__':
    DEBUG('@:blueprintCoreSite: debug run')
