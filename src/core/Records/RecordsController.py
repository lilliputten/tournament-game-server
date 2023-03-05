# -*- coding:utf-8 -*-
# @module RecordsController
# @desc Records controller utils
# @since 2023.03.05, 01:34
# @changed 2023.03.05, 23:36


from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .RecordsStorage import recordsStorage
from src.core.lib.gameHelpers import getFirstSortedGameRecords


class RecordsController(Storage):

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def addRecord(self, gameRecord):
        Token = gameRecord['Token']
        recordsStorage.addRecord(Token=Token, data=gameRecord)

    def getRecentRecords(self):
        # TODO: Get gameMode and filter records with it?
        # Find {recordsTableS} recent results sorted by winnerRatio
        allRecords = recordsStorage.getAllData()
        recentRecords = getFirstSortedGameRecords(allRecords)
        return recentRecords


# Create singleton...
recordsController = RecordsController()


__all__ = [  # Exporting objects...
    'recordsController',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
