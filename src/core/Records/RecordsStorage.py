# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Storage for game records
# @since 2023.03.05, 01:34
# @changed 2023.03.19, 03:24


from typing_extensions import TYPE_CHECKING
from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from src.core.types.RecordsTypes import TGameRecord
from . import RecordsConstants


class RecordsStorage(Storage[TGameRecord]):

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
