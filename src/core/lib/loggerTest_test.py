# -*- coding:utf-8 -*-
# @module loggerTest_test
# @desc Sample test module
# @since 2022.02.15, 05:02
# @changed 2022.02.15, 05:02

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k loggerTest`
#  - `python -m unittest -f src/core/loggerTest_test.py`

import unittest

from src.core.lib import utils

#  from src.core.lib.loggerTest import test
from .loggerTest import test


#  test = True


print('\nRunning tests for', utils.getTrace())


class Test_loggerTest(unittest.TestCase):

    def test_case_1(self):
        print('\nRunning test', utils.getTrace())
        self.assertEqual(test, True)


if __name__ == '__main__':
    unittest.main()
