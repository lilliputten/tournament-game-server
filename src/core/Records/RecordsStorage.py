# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Storage for game records
# @since 2023.03.05, 01:34
# @changed 2023.03.05, 01:34


from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from . import RecordsConstants


class RecordsStorage(Storage):

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode
        super().__init__(testMode, dbName=RecordsConstants.dbName)


# Create singleton...
recordsStorage = RecordsStorage()


__all__ = [  # Exporting objects...
    'recordsStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
