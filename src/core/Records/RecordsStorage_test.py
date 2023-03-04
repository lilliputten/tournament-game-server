# -*- coding:utf-8 -*-
# @module RecordsStorage_test
# @since 2023.03.05, 01:34
# @changed 2023.03.05, 01:34

# @see https://docs.python.org/3/library/unittest.html
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k RecordsStorage`
#  - `python -m unittest -f src/core/Records/RecordsStorage_test.py`

import datetime
import unittest

from tinydb import Query

from src.core.lib.utils import getTrace
from src.core.lib.logger import (
    getMsTimeStamp,
)

from .RecordsStorage import RecordsStorage


print('\nRunning tests for', getTrace())


relevanceTime = 10

recordsStorage = RecordsStorage(testMode=True)


class Test_recordsStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initializations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        recordsStorage.clearData()

    def test_addRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', getTrace())
        recordsStorage.addRecord(Token='test', data={'value': 'new record'})
        recordsStorage.dbSave()
        recordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 1)


if __name__ == '__main__':
    unittest.main()
