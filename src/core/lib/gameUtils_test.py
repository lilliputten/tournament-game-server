import unittest

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .gameUtils import getGameTimestamps, getLatestGameTimestamp


class Test_gameUtils(unittest.TestCase):

    def test_getGameTimestamps(self):
        """
        getGameTimestamps
        """
        print('\nRunning test', getTrace())
        gameRecord = {
            'timestamp': 1,
            'lastActivityTimestamp': 2,
        }
        results = getGameTimestamps(gameRecord)
        self.assertTrue(results == [1, 2])

    def test_getLatestGameTimestamp(self):
        """
        getLatestGameTimestamp
        """
        print('\nRunning test', getTrace())
        gameRecord = {
            'timestamp': 1,
            'lastActivityTimestamp': 2,
        }
        result = getLatestGameTimestamp(gameRecord)
        self.assertTrue(result == 2)


if __name__ == '__main__':
    DEBUG(getTrace(' test run'))
    unittest.main()
