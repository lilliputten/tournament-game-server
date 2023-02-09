# -*- coding: utf-8 -*-
# vim: ft=python:
# @module gunicorn.py
# @desc Local server start script (for start with gunicorn; see `utils/rpi-start-server.sh`)
# @since 2022.02.07, 21:30
# @changed 2022.02.24, 04:44

import sys
import os

#  # Activate venv (UNUSED for local device?)...
#  venv = 'venv-py3-flask'  # Python 3.6
#  #  venv = 'virtualenv'  # Default
#  #  venv = 'venv-flask'  # Python 2.7
#  activate_this = '/home/g/goldenjeru/.' + venv + '/bin/activate_this.py'
#  with open(activate_this) as f:
#      code = compile(f.read(), activate_this, 'exec')
#      exec(code, dict(__file__=activate_this))

# Inject application path...
rootPath = os.path.dirname(os.path.abspath(__file__))  # From index.wsgi
sys.path.insert(1, rootPath)  # /home/g/goldenjeru/lilliputten.ru/cam-rpi-server/

os.environ['GUNICORN_ENV'] = 'default'

# Start application...
from src.server import app as application  # noqa  # pylint: disable=wrong-import-position

__all__ = [  # Exporting objects...
    'application',
]

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
