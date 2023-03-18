# -*- coding:utf-8 -*-
# @module GameStorage
# @desc Storage for game sessions
# @since 2023.02.13, 13:52
# @changed 2023.03.19, 03:24


from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from src.core.types.RecordsTypes import TGameRecord
from . import GameConstants


class GameStorage(Storage[TGameRecord]):

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode
        super().__init__(testMode, dbName=GameConstants.dbName)


# Create singleton...
gameStorage = GameStorage()


__all__ = [  # Exporting objects...
    'gameStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
