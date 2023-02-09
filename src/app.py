# -*- coding:utf-8 -*-
# @module app
# @since 2022.02.07, 00:27
# @changed 2022.02.07, 00:27

import os
from flask import Flask
#  from flask import session
from flask_cors import CORS
from werkzeug.routing import BaseConverter
from src.core.lib.logger import DEBUG

from config import config


#  rootPath = config['rootPath']
clientStaticPath = config['clientStaticPath']
clientTemplatePath = config['clientTemplatePath']
clientStaticUrl = config['clientStaticUrl']

DEBUG('@:app: starting', {
    'clientStaticPath': clientStaticPath,
    'clientTemplatePath': clientTemplatePath,
    'clientStaticUrl': clientStaticUrl,
})


secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'

app = Flask(__name__,
            static_url_path=clientStaticUrl,
            #  static_url_path='',
            static_folder=clientStaticPath)
app.secret_key = secret_key
#  app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = secret_key
#  app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['CORS_HEADERS'] = 'Content-Type'


CORS(
    app,
    expose_headers='Authorization',
    allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
    supports_credentials=True,
    resources={
        # https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#sending_a_request_with_credentials_included
        # Note: Access-Control-Allow-Origin is prohibited from using a wildcard
        # for requests with credentials: 'include'. In such cases, the exact
        # origin must be provided; even if you are using a CORS unblocker
        # extension, the requests will still fail.
        r'*': {
            #  'origins': '*',
            'origins': config['legalOrigins'],
        },
    },
)
# Check OPTIONS request:
# curl -v -H "Authorization: Basic YXBpOnB1c3BsbmR2cWFpdmJ5bnY=" \
# -X OPTIONS https://back.march.team/api/v1.0/start
# Configure precise origins:
# api_v1_cors_config = {
#   "origins": ["http://localhost:5000"]
# }
# CORS(app, resources={"/api/v1/*": api_v1_cors_config})


@app.template_filter()
def getenv(key):
    return os.getenv(key)


class ListConverter(BaseConverter):
    regex = r'\S+(?:,\d+)*,?'

    def to_python(self, value):
        return [str(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)


app.url_map.converters['list'] = ListConverter

__all__ = [  # Exporting objects...
    'app',
    'secret_key',
]
