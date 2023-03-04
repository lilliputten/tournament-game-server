import unittest
import json
from os import path

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .gameHelpers import determineGameWinner, getCorrectQuestionAnswersCount, getGameTimestamps, getLatestGameTimestamp

currPath = path.dirname(path.abspath(__file__))


# Load real game record dump for tests...
testJsonFilename = 'gameHelpers-testData-01.json'
testJsonFilepath = path.join(currPath, testJsonFilename)
testJsonData = None
if path.isfile(testJsonFilepath):
    with open(testJsonFilepath, encoding='utf-8') as file:
        testJsonData = json.load(file)


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


if __name__ == '__main__':
    DEBUG(getTrace(' test run'))
    unittest.main()
