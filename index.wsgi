# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Fullspace hosting server start script
# @since 2019.03.28, 21:32
# @changed 2023.02.09, 22:01

import sys  # noqa
import os  # noqa

venv = 'venv-py3.10-flask'  # Python 3.10
#  venv = 'venv-py3-flask'  # Python 3.6
#  venv = 'virtualenv'  # Default
#  venv = 'venv-flask'  # Python 2.7

# Activate venv...
activate_this = '/home/g/goldenjeru/.' + venv + '/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# TODO: Reuse `index.py`?

# Inject application path...
rootPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, rootPath)  # noqa  # pylint: disable=wrong-import-position

# Start application...
from src.server import app as application  # noqa

__all__ = [  # Exporting objects...
    'application',
]
