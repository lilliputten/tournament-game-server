# -*- coding:utf-8 -*-
# @module RecordsController
# @desc Records controller utils
# @since 2023.03.05, 01:34
# @changed 2023.03.17, 12:03


from flask import request
from tinydb import Query
from src import appSession
from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .RecordsStorage import recordsStorage
from src.core.lib.gameHelpers import getSortedGameRecords


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
        args = request.args
        all = args.get('all')
        # Find records for current game mode...
        gameMode = appSession.getVariable('gameMode') if all is None or not all else ''
        recordsStorage.dbSync()
        if gameMode is None or not gameMode:
            allRecords = recordsStorage.getAllData()
        else:
            q = Query()
            # TODO: Add filter by questions set
            findQuery = (q.gameMode == gameMode)
            allRecords = recordsStorage.findRecords(findQuery)
        recentRecords = getSortedGameRecords(allRecords)
        return recentRecords


# Create singleton...
recordsController = RecordsController()


__all__ = [  # Exporting objects...
    'recordsController',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
