# -*- coding:utf-8 -*-
# @module RequestsStorageSingleton
# @since 2022.03.25, 19:19
# @changed 2022.03.25, 19:19


#  from src.core.lib.logger import DEBUG
from src.core.lib import utils

from .RequestsStorage import RequestsStorage


# Create singleton...
requestsStorage = RequestsStorage()


__all__ = [  # Exporting objects...
    'requestsStorage',
]


if __name__ == '__main__':
    print(utils.getTrace(), 'debug run')
