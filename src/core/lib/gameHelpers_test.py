import unittest
#  import json
from os import path

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .gameHelpers import determineGameWinner, getCorrectQuestionAnswersCount, getSortedGameRecordTokens, getGameRecordRatio, getGameTimestamps, getLatestGameTimestamp

currPath = path.dirname(path.abspath(__file__))


#  # Load real game record dump for tests...
#  testJsonFilename = 'gameHelpers-testData-01.json'
#  testJsonFilepath = path.join(currPath, testJsonFilename)
#  testJsonData = None
#  if path.isfile(testJsonFilepath):
#      with open(testJsonFilepath, encoding='utf-8') as file:
#          testJsonData = json.load(file)


# @see https://www.geeksforgeeks.org/python-unittest-assertequal-function/


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

    def test_getCorrectQuestionAnswersCount_0(self):
        """
        getCorrectQuestionAnswersCount_0
        """
        print('\nRunning test', getTrace())
        questionAnswers = {}
        result = getCorrectQuestionAnswersCount(questionAnswers)
        self.assertEqual(result, 0, 'Should not found correct answers')

    def test_getCorrectQuestionAnswersCount_1(self):
        """
        getCorrectQuestionAnswersCount_1
        """
        print('\nRunning test', getTrace())
        questionAnswers = {
            'q1': 'correct',
            'q2': 'wrong',
        }
        result = getCorrectQuestionAnswersCount(questionAnswers)
        self.assertEqual(result, 1, 'Should found 1 answer')

    def test_getCorrectQuestionAnswersCount_2(self):
        """
        getCorrectQuestionAnswersCount_2
        """
        print('\nRunning test', getTrace())
        questionAnswers = {
            'q0': 'correct',
            'q1': 'correct',
            'q2': 'wrong',
        }
        result = getCorrectQuestionAnswersCount(questionAnswers)
        self.assertEqual(result, 2, 'Should found 2 correct answers')

    def test_determineGameWinner_byAnswersCount(self):
        """
        determineGameWinner_byAnswersCount
        """
        print('\nRunning test', getTrace())
        gameRecord = {
            'startedTimestamp': 0,
            'finishedTimestamp': 20,
            'partners': [
                'player-1',
                'player-2',
            ],
            'partnersInfo': {
                'player-1': {
                    'questionAnswers': {
                        'Q1': 'correct',
                    },
                    'finishedTimestamp': 20,
                },
                'player-2': {
                    'questionAnswers': {
                        'Q1': 'wrong',
                    },
                    'finishedTimestamp': 10,
                },
            },
        }
        expectedToken = 'player-1'
        result = determineGameWinner(gameRecord)
        self.assertEqual(result, expectedToken, 'Should found correct token for maximum answered questions')

    def test_determineGameWinner_fastest(self):
        """
        determineGameWinner_fastest
        """
        print('\nRunning test', getTrace())
        gameRecord = {
            'startedTimestamp': 0,
            'finishedTimestamp': 20,
            'partners': [
                'player-1',
                'player-2',
            ],
            'partnersInfo': {
                'player-1': {
                    'questionAnswers': {
                        'Q1': 'correct',
                    },
                    'finishedTimestamp': 20,
                },
                'player-2': {
                    'questionAnswers': {
                        'Q1': 'correct',
                    },
                    'finishedTimestamp': 10,
                },
            },
        }
        expectedToken = 'player-2'
        result = determineGameWinner(gameRecord)
        self.assertEqual(result, expectedToken, 'Should found correct token for minimal gameplay time')

    # getGameRecordRatio:

    def test_getGameRecordRatio_rangeForRealLargeTimes(self):
        """
        getGameRecordRatio rangeForRealLargeTimes
        """
        print('\nRunning test', getTrace())
        record = {
            'Token': 'game-1',
            'winnerToken': 'player-1',
            'startedTimestamp': 0,
            'partners': [
                'player-1',
            ],
            'partnersInfo': {
                'player-1': {
                    'questionAnswers': {
                        # 10 answers, 5 of them is correct (answers ratio is 1/2)
                        'Q0': 'wrong',
                        'Q1': 'wrong',
                        'Q2': 'wrong',
                        'Q3': 'wrong',
                        'Q4': 'wrong',
                        'Q5': 'correct',
                        'Q6': 'correct',
                        'Q7': 'correct',
                        'Q8': 'correct',
                        'Q9': 'correct',
                    },
                    'finishedTimestamp': 1000 * 60 * 20,  # 20 min
                },
            },
        }
        ratio = getGameRecordRatio(record)
        self.assertTrue(ratio > 1 and ratio < 10000, 'Ratios should be enought large numbers (for large times, > 10 mins)')

    def test_getGameRecordRatio_rangeForRealSmallTimes(self):
        """
        getGameRecordRatio rangeForRealSmallTimes
        """
        print('\nRunning test', getTrace())
        record = {
            'Token': 'game-1',
            'winnerToken': 'player-1',
            'startedTimestamp': 0,
            'partners': [
                'player-1',
            ],
            'partnersInfo': {
                'player-1': {
                    'questionAnswers': {
                        # 10 answers, 5 of them is correct (answers ratio is 1/2)
                        'Q0': 'wrong',
                        'Q1': 'wrong',
                        'Q2': 'wrong',
                        'Q3': 'wrong',
                        'Q4': 'wrong',
                        'Q5': 'correct',
                        'Q6': 'correct',
                        'Q7': 'correct',
                        'Q8': 'correct',
                        'Q9': 'correct',
                    },
                    'finishedTimestamp': 1000 * 5,  # 5 sec
                },
            },
        }
        ratio = getGameRecordRatio(record)
        self.assertTrue(ratio > 1 and ratio < 10000, 'Ratios should be enought large numbers (for small times, < 10 secs)')

    def test_getGameRecordRatio_noCorrectAnswers(self):
        """
        getGameRecordRatio noCorrectAnswers
        """
        print('\nRunning test', getTrace())
        record = {
            'Token': 'game-1',
            'winnerToken': 'player-1',
            'startedTimestamp': 0,
            'partners': [
                'player-1',
            ],
            'partnersInfo': {
                'player-1': {
                    'questionAnswers': {
                        # No correct answers (answers ratio is 0 -- overall ratio is 0 too)
                        'Q1': 'wrong',
                    },
                    'finishedTimestamp': 1000,  # Any time
                },
            },
        }
        ratio = getGameRecordRatio(record)
        self.assertEqual(ratio, 0, 'Ratio for zero number of correct answers should be 0')

    # getSortedGameRecordTokens:

    def test_getSortedGameRecordTokens_simple(self):
        """
        getSortedGameRecordTokens simple
        """
        print('\nRunning test', getTrace())
        records = [
            {
                'Token': 'game-1',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
                'partners': [
                    'player-1',
                ],
                'partnersInfo': {
                    'player-1': {
                        'questionAnswers': {
                            'Q1': 'correct',
                        },
                        'finishedTimestamp': 20,
                    },
                },
            },
            {
                'Token': 'game-2',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
                'partners': [
                    'player-1',
                ],
                'partnersInfo': {
                    'player-1': {
                        'questionAnswers': {
                            'Q1': 'correct',
                        },
                        'finishedTimestamp': 10,
                    },
                },
            },
        ]
        expectedTokens = ['game-2', 'game-1']
        resultTokens = getSortedGameRecordTokens(records, None)
        self.assertEqual(resultTokens, expectedTokens, 'Should return correctly sorted tokens list')

    def test_getSortedGameRecordTokens_truncateResults(self):
        """
        getSortedGameRecordTokens truncateResults
        """
        print('\nRunning test', getTrace())
        records = [
            {
                'Token': 'game-1',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
                'partners': [
                    'player-1',
                ],
                'partnersInfo': {
                    'player-1': {
                        'questionAnswers': {
                            'Q1': 'correct',
                        },
                        'finishedTimestamp': 20,
                    },
                },
            },
            {
                'Token': 'game-2',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
                'partners': [
                    'player-1',
                ],
                'partnersInfo': {
                    'player-1': {
                        'questionAnswers': {
                            'Q1': 'correct',
                        },
                        'finishedTimestamp': 10,
                    },
                },
            },
        ]
        resultTokens = getSortedGameRecordTokens(records, 1)
        self.assertEqual(len(resultTokens), 1, 'Results should be trunctated if specified parameter `recordsTableSize`')


# getSortedGameRecordTokens:
# - Test truncate records with recordsTableSize

if __name__ == '__main__':
    DEBUG(getTrace(' test run'))
    unittest.main()
