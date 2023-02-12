# -*- coding:utf-8 -*-
# @module WaitingStorage_test
# @since 2023.02.12, 01:01
# @changed 2023.02.12, 01:42

# @see https://docs.python.org/3/library/unittest.html
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k WaitingStorage`
#  - `python -m unittest -f src/core/Records/WaitingStorage_test.py`

import datetime
#  import time
import unittest
import functools

from tinydb import Query

#  from src.core.lib import utils
# from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
from src.core.lib.logger import (
    #  getDateStr,
    getMsTimeStamp,
)

from .WaitingStorage import WaitingStorage


print('\nRunning tests for', getTrace())


relevanceTime = 10

waitingStorage = WaitingStorage(testMode=True)


class Test_waitingStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initialisations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        waitingStorage.clearData()

    def test_getEmptyData(self):
        """
        Empty list must be returned for empty database.
        """
        print('\nRunning test', getTrace())
        records = waitingStorage.getAllData()
        self.assertEqual(len(records), 0)

    def test_emptyData(self):
        """
        Test initial (empty) state.
        """
        print('\nRunning test', getTrace())
        self.assertEqual(waitingStorage.getRecordsCount(), 0)

    def test_addRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', getTrace())
        waitingStorage.addRecord(Token='test', data={'value': 'new record'})
        waitingStorage.dbSave()
        recordsCount = waitingStorage.getRecordsCount()
        self.assertEqual(recordsCount, 1)

    def test_findRecords(self):
        """
        Test of getting of records by parameter (`Token`).
        """
        print('\nRunning test', getTrace())
        waitingStorage.addRecord(Token='test', data={'value': 'must be found'})
        waitingStorage.addRecord(Token='other', data={'value': 222})
        foundRecords = waitingStorage.findRecords({'Token': 'test'})
        self.assertEqual(len(foundRecords), 1)

    def test_findRecordsWithCustomFunc(self):
        """
        Test of getting of records by custom comparator function.
        """
        print('\nRunning test', getTrace())
        waitingStorage.addRecord(Token='test', data={'value': 'must be found'})
        waitingStorage.addRecord(Token='other', data={'value': 222})

        def customFunc(recordValue, value):
            return recordValue == value  # noqa: E731  # use def instead lambda

        with waitingStorage.getDbHandler() as db:
            if db is not None:
                Test = Query()
                foundRecords = db.search(Test.value.test(customFunc, 'must be found'))  # type: ignore
                foundRecordsCount = len(foundRecords)
                self.assertEqual(foundRecordsCount, 1)

    def test_removeRecords(self):
        """
        Test of removing of records by parameters (`Token`).
        """
        print('\nRunning test', getTrace())
        waitingStorage.addRecord(Token='test', data={'value': 'must be found and removed'})
        waitingStorage.addRecord(Token='other', data={'value': 'must be remained'})
        waitingStorage.addRecord(Token='test', data={'value': 'must be found and removed'})
        waitingStorage.addRecord(Token='other', data={'value': 'must be remained'})
        waitingStorage.removeRecords({'Token': 'test'})
        remainedRecordsCount = waitingStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)

    def test_extractRecords(self):
        """
        Test of extracing (finding & removing) of records by parameters (`Token`).
        """
        print('\nRunning test', getTrace())
        waitingStorage.addRecord(Token='test', data={'value': 'must be found and removed'})
        waitingStorage.addRecord(Token='other', data={'value': 'must be remained'})
        waitingStorage.addRecord(Token='test', data={'value': 'must be found and removed'})
        waitingStorage.addRecord(Token='other', data={'value': 'must be remained'})
        removedRecords = waitingStorage.extractRecords({'Token': 'test'})
        # Check removed records...
        # 2 records must be removed...
        self.assertEqual(len(removedRecords), 2)
        # Check which records was removed...
        removedRecordsValues = list(map(lambda record: record['value'], removedRecords))
        removedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be found and removed'), removedRecordsValues, True)
        self.assertEqual(removedRecordsTest, True)
        # Check removed records...
        # 2 records must be remained
        remainedRecordsCount = waitingStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)
        # Check which records was removed...

        # TODO: Fetch all data...
        remainedRecords = waitingStorage.getAllData()
        remainedRecordsValues = list(map(lambda record: record['value'], remainedRecords))
        remainedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be remained'), remainedRecordsValues, True)
        self.assertEqual(remainedRecordsTest, True)

    def test_addObsoleteRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', getTrace())
        now = datetime.datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        oldTimestamp = timestamp - relevanceTime
        waitingStorage.addRecord(Token='test', timestamp=oldTimestamp, data={'value': 'old (should be removed)'})
        waitingStorage.addRecord(Token='other', timestamp=timestamp, data={'value': 'new (should be preserved)'})
        tokenFragment = {'Token': 'test'}
        tokenQuery = Query().fragment(tokenFragment)
        q = Query()
        timeQuery = q.timestamp < timestamp
        testQuery = tokenQuery | timeQuery
        removedRecords = waitingStorage.extractRecords(testQuery)
        waitingStorage.dbSave()
        recordsCount = waitingStorage.getRecordsCount()
        # Should remove old record and remain new
        self.assertEqual(recordsCount, 1)
        self.assertEqual(len(removedRecords), 1)
        removedValue = removedRecords[0]['value']
        self.assertEqual(removedValue, 'old (should be removed)')


if __name__ == '__main__':
    unittest.main()
