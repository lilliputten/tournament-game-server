# -*- coding:utf-8 -*-
# @module RequestsStorage_test
# @since 2022.03.25, 19:19
# @changed 2022.03.25, 23:53

# @see https://docs.python.org/3/library/unittest.html
# @see https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k RequestsStorage`
#  - `python -m unittest -f src/core/Records/RequestsStorage_test.py`

#  import time
import unittest
# import functools

from src.core.lib import utils

from . import RequestsMail


print('\nRunning tests for', utils.getTrace())

testData = {
    'Name': 'Test',
    'ip': '127.0.0.1',
    'recordType': None,
    'requestType': 'Test',
    'Token': '220325-220958-241-2259080',
    'timestamp': 1648238358086,
    'timestr': '2022.03.25 22:59:18'
}


class Test_RequestsMail(unittest.TestCase):

    #  def setUp(self):  # TODO: Initialisations before each test

    #  def tearDown(self):  # Made cleanups after each test
    #      """
    #      Made cleanups after each test
    #      """
    #      recordsStorage.clearData()

    def test_createRecordMailMsg(self):
        """
        Create mail message for request data.
        """
        print('\nRunning test', utils.getTrace())
        msg = RequestsMail.createRecordMailMsg(testData)
        self.assertRegex(msg, r'<h2.*Тестовый запрос')

    #  def test_sendRecordMail(self):
    #      """
    #      Create mail message for request data.
    #      """
    #      print('\nRunning test', utils.getTrace())
    #      RequestsMail.sendRecordMail(testData)
    #      #  self.assertRegex(msg, r'<h2.*Тестовый запрос')


if __name__ == '__main__':
    unittest.main()
