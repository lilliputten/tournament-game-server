# -*- coding:utf-8 -*-
# @module __init__
# @since 2022.02.07, 00:27
# @changed 2022.02.07, 00:27

#  from flask import Flask
#  app = Flask('server')

import os
import sys

if os.getenv('FLASK_ENV') == 'development':
    sys.dont_write_bytecode = True
