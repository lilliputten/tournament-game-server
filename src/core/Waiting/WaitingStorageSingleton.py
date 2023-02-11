# -*- coding:utf-8 -*-
# @module WaitingStorageSingleton
# @since 2023.02.12, 01:01
# @changed 2023.02.12, 01:42


#  from src.core.lib.logger import DEBUG
from src.core.lib import utils

from .WaitingStorage import WaitingStorage


# Create singleton...
waitingStorage = WaitingStorage()


__all__ = [  # Exporting objects...
    'waitingStorage',
]


if __name__ == '__main__':
    print(utils.getTrace(), 'debug run')
