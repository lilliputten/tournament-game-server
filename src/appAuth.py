# -*- coding:utf-8 -*-
# @module appAuth
# @since 2023.02.10, 15:23
# @changed 2023.02.10, 15:23

from flask_httpauth import HTTPBasicAuth

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

auth = HTTPBasicAuth()

DEBUG('@:appAuth: starting')


@auth.verify_password
def authenticate(username, password):
    DEBUG(getTrace(), {
        'username': username,
        'password': password,
    })
    if username and password:
        if username == config['apiUser'] and password == config['apiPass']:
            return True
    return False


__all__ = [  # Exporting objects...
    'auth',
]

if __name__ == '__main__':
    DEBUG('@:blueprintRootApi: debug run')
