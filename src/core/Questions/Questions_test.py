# -*- coding:utf-8 -*-
# @module Questions_test
# @since 2023.02.15, 01:53
# @changed 2023.02.15, 02:26

# @see https://docs.python.org/3/library/unittest.html
# @see: https://tinydb.readthedocs.io/en/latest/usage.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k Questions`
#  - `python -m unittest -f src/core/Records/Questions_test.py`

# import datetime
import unittest

#  from src.core.lib import utils
from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
# from src.core.lib.logger import (
#     #  getDateStr,
#     getMsTimeStamp,
# )

from .Questions import Questions


print('\nRunning tests for', getTrace())


questions = Questions(testMode=True)


class Test_gameStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initializations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        pass

    def test_getFileName(self):
        """
        getFileName
        """
        print('\nRunning test', getTrace())
        fileName = questions.getFileName()
        DEBUG(getTrace('test'), {
            'fileName': fileName,
        })
        self.assertTrue(fileName)

    def test_loadQuestions(self):
        """
        loadQuestions
        """
        print('\nRunning test', getTrace())
        data = questions.loadQuestions()
        DEBUG(getTrace('test'), {
            'data': data,
        })
        self.assertTrue(data)

    def test_getClientQuestionsData(self):
        """
        getClientQuestionsData
        """
        print('\nRunning test', getTrace())
        data = questions.getClientQuestionsData()
        DEBUG(getTrace('test'), {
            'data': data,
        })
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
