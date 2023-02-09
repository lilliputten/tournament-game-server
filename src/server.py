# -*- coding:utf-8 -*-
# @module server
# @since 2022.02.07, 00:27
# @changed 2022.03.27, 20:37

import os

from config import config
#  from .appSocketIO import appSocketIO

from src.core.lib.utils import getTrace
from src.core.lib.logger import DEBUG

from src.app import app


# Try to avoid twice starting bug...
run_main = os.environ.get('WERKZEUG_RUN_MAIN')
isMain = run_main == 'true'
doInit = not config['isDev'] or isMain

if doInit:  # NOTE: Initializing only once (avoiding double initialization with `* Restarting with stat`...)

    #  from externalApi import externalApi
    #  from flask import jsonify
    #  from flask import redirect
    #  from flask import render_template
    #  from flask import request
    #  from flask import url_for

    from . import serverUtils
    #  from .blueprintTest import blueprintTest
    from .blueprintCoreSite import blueprintCoreSite
    from .blueprintRootApi import blueprintRootApi
    from .blueprintRequests import blueprintRequests

    DEBUG(getTrace('starting'), {
        'doInit': doInit,
        'isDev': config['isDev'],
        'isMain': isMain,
        'isGunicorn': config['isGunicorn'],
        'isRPi': config['isRPi'],
        'flaskEnv': config['flaskEnv'],
        'gunicornEnv': config['gunicornEnv'],
        'run_main': run_main,
        #  'FLASK_ENV': os.getenv('FLASK_ENV'),
        'buildTag': config['buildTag'],
        #  'HTTP_STATUS_CODES': HTTP_STATUS_CODES,
    })

    #  Register blueprint apis...

    #  app.register_blueprint(blueprintTest)
    app.register_blueprint(blueprintCoreSite)
    app.register_blueprint(blueprintRootApi)
    app.register_blueprint(blueprintRequests)

    # Errors handling...

    @app.errorhandler(404)
    def handle_not_found(err):
        return serverUtils.server_handle_not_found(err)

    @app.errorhandler(Exception)
    def handle_exception(err):
        return serverUtils.server_handle_exception(err)


if __name__ == '__main__':
    app.secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'
    #  print('server:__main__')
    #  app.logger.debug('test log')
    # app.debug = True
    #  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    app.run()
