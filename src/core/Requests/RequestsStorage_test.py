# -*- coding:utf-8 -*-
# @module RequestsStorage_test
# @since 2022.03.25, 19:19
# @changed 2022.03.26, 01:09

# @see https://docs.python.org/3/library/unittest.html
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k RequestsStorage`
#  - `python -m unittest -f src/core/Records/RequestsStorage_test.py`

#  import time
import unittest
import functools

from tinydb import Query

from src.core.lib import utils

from .RequestsStorage import RequestsStorage


print('\nRunning tests for', utils.getTrace())


#  relevanceTime = 10

requestsStorage = RequestsStorage(testMode=True)


class Test_requestsStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initialisations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        requestsStorage.clearData()

    def test_getEmptyData(self):
        """
        Empty list must be returned for empty database.
        """
        print('\nRunning test', utils.getTrace())
        records = requestsStorage.getAllData()
        self.assertEqual(len(records), 0)

    def test_emptyData(self):
        """
        Test initial (empty) state.
        """
        print('\nRunning test', utils.getTrace())
        self.assertEqual(requestsStorage.getRecordsCount(), 0)

    def test_addedRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', utils.getTrace())
        requestsStorage.addRecord(requestType='test', data={'value': 'new record'})
        requestsStorage.dbSave()
        recordsCount = requestsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 1)

    def test_findRecords(self):
        """
        Test of getting of records by parameter (`requestType`).
        """
        print('\nRunning test', utils.getTrace())
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found'})
        requestsStorage.addRecord(requestType='other', data={'value': 222})
        foundRecords = requestsStorage.findRecords({'requestType': 'test'})
        self.assertEqual(len(foundRecords), 1)

    def test_findRecordsWithCustomFunc(self):
        """
        Test of getting of records by custom comparator funciton.
        """
        print('\nRunning test', utils.getTrace())
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found'})
        requestsStorage.addRecord(requestType='other', data={'value': 222})

        def customFunc(recordValue, value):
            return recordValue == value  # noqa: E731  # use def instead lambda

        with requestsStorage.getDbHandler() as db:
            if db is not None:
                Test = Query()
                foundRecords = db.search(Test.value.test(customFunc, 'must be found'))
                foundRecordsCount = len(foundRecords)
                self.assertEqual(foundRecordsCount, 1)

    def test_removeRecords(self):
        """
        Test of removing of records by parameters (`requestType`).
        """
        print('\nRunning test', utils.getTrace())
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found and removed'})
        requestsStorage.addRecord(requestType='other', data={'value': 'must be remained'})
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found and removed'})
        requestsStorage.addRecord(requestType='other', data={'value': 'must be remained'})
        requestsStorage.removeRecords({'requestType': 'test'})
        remainedRecordsCount = requestsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)

    def test_extractRecords(self):
        """
        Test of extracing (finding & removing) of records by parameters (`requestType`).
        """
        print('\nRunning test', utils.getTrace())
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found and removed'})
        requestsStorage.addRecord(requestType='other', data={'value': 'must be remained'})
        requestsStorage.addRecord(requestType='test', data={'value': 'must be found and removed'})
        requestsStorage.addRecord(requestType='other', data={'value': 'must be remained'})
        removedRecords = requestsStorage.extractRecords({'requestType': 'test'})
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
        remainedRecordsCount = requestsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)
        # Check which records was removed...

        # TODO: Fetch all data...
        remainedRecords = requestsStorage.getAllData()
        remainedRecordsValues = list(map(lambda record: record['value'], remainedRecords))
        remainedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be remained'), remainedRecordsValues, True)
        self.assertEqual(remainedRecordsTest, True)


if __name__ == '__main__':
    unittest.main()
