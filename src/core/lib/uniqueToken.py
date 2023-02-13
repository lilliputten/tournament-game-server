# -*- coding:utf-8 -*-
# @module uniqueToken
# @desc Creates unique token
# @since 2023.02.13, 13:31
# @changed 2023.02.13, 13:31

import uuid
import random
import datetime

from flask import session

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getMsDateTag,
)

from src.core.lib.utils import getTrace

isDev = config['isDev']
useSimplifiedSessionId = isDev


def createUniqueToken():
    """
    Create unique token
    """
    Token = session.get('Token')
    now = datetime.datetime.now()  # Get current date object
    dateTag = getMsDateTag(now)
    # Create random token id (simple for dev mode or uuid for production)
    sesseionIdValue = random.randint(100000, 10000000) if useSimplifiedSessionId else uuid.uuid4()
    # Compose token value using date tag and unique id; TODO: Use PyJWT encoding?
    Token = dateTag + '-' + str(sesseionIdValue)
    return Token


__all__ = [  # Exporting objects...
    'createUniqueToken',
]


if __name__ == '__main__':
    DEBUG(getTrace('debug run'))
