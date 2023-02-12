# -*- coding:utf-8 -*-
# @module WaitingStorage
# @desc Storage for waiting records
# @since 2023.02.12, 01:01
# @changed 2023.02.12, 20:46


from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from src.core.Waiting import WaitingConstants


class WaitingStorage(Storage):

    def __init__(self, testMode=False):
        super().__init__(testMode, dbName=WaitingConstants.dbName)


__all__ = [  # Exporting objects...
    'WaitingStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
