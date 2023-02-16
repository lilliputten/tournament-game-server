# -*- coding:utf-8 -*-
# @module GameStorage_test
# @since 2023.02.13, 13:52
# @changed 2023.02.13, 13:52

# @see https://docs.python.org/3/library/unittest.html
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k GameStorage`
#  - `python -m unittest -f src/core/Records/GameStorage_test.py`

import datetime
import unittest

from tinydb import Query

from src.core.lib.utils import getTrace
from src.core.lib.logger import (
    getMsTimeStamp,
)

from .GameStorage import GameStorage


print('\nRunning tests for', getTrace())


relevanceTime = 10

gameStorage = GameStorage(testMode=True)


class Test_gameStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initializations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        gameStorage.clearData()

    def test_addRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', getTrace())
        gameStorage.addRecord(Token='test', data={'value': 'new record'})
        gameStorage.dbSave()
        recordsCount = gameStorage.getRecordsCount()
        self.assertEqual(recordsCount, 1)

    def test_addObsoleteRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', getTrace())
        now = datetime.datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        oldTimestamp = timestamp - relevanceTime
        gameStorage.addRecord(Token='test', timestamp=oldTimestamp, data={'value': 'old (should be removed)'})
        gameStorage.addRecord(Token='other', timestamp=timestamp, data={'value': 'new (should be preserved)'})
        tokenFragment = {'Token': 'test'}
        tokenQuery = Query().fragment(tokenFragment)
        q = Query()
        timeQuery = q.timestamp < timestamp
        testQuery = tokenQuery | timeQuery
        removedRecords = gameStorage.extractRecords(testQuery)
        gameStorage.dbSave()
        recordsCount = gameStorage.getRecordsCount()
        # Should remove old record and remain new
        self.assertEqual(recordsCount, 1)
        self.assertEqual(len(removedRecords), 1)
        removedValue = removedRecords[0]['value']
        self.assertEqual(removedValue, 'old (should be removed)')


if __name__ == '__main__':
    unittest.main()
