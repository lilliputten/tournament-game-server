import unittest
# @see https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug

from os import path
from typing import List

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace
from src.core.types.RecordsTypes import TGameRecord, TRecordData

from .gameHelpers import (
    maxRatio,
    determineGameWinner,
    getCorrectQuestionAnswersCount,
    getSortedGameRecords,
    getGameTimestamps,
    getLatestGameTimestamp,
    prepareRecordsData,
    findMinStartedTimestamp,
    findMaxFinishedTimestamp,
    findRecordsDuration,
    getGameRecordRatioNumber,
    getGameRecordRatioTag,
)

currPath = path.dirname(path.abspath(__file__))


#  # Load real game record dump for tests...
#  testJsonFilename = 'gameHelpers-testData-01.json'
#  testJsonFilepath = path.join(currPath, testJsonFilename)
#  testJsonData = None
#  if path.isfile(testJsonFilepath):
#      with open(testJsonFilepath, encoding='utf-8') as file:
#          testJsonData = json.load(file)


# @see https://www.geeksforgeeks.org/python-unittest-assertequal-function/


class Test_gameHelpers(unittest.TestCase):

    def test_getGameTimestamps(self):
        """
        getGameTimestamps
        """
        print('\nRunning test', getTrace())
        gameRecord: TGameRecord = {  # pyright: ignore
            'timestamp': 1,
            'lastCheckTimestamp': 2,
        }
        results = getGameTimestamps(gameRecord)
        self.assertTrue(results == [1, 2])

    def test_getLatestGameTimestamp(self):
        """
        getLatestGameTimestamp
        """
        print('\nRunning test', getTrace())
        gameRecord: TGameRecord = {  # pyright: ignore
            'timestamp': 1,
            'lastCheckTimestamp': 2,
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
        gameRecord: TGameRecord = {  # pyright: ignore
            'startedTimestamp': 0,
            'finishedTimestamp': 20,
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
        gameRecord: TGameRecord = {  # pyright: ignore
            'startedTimestamp': 0,
            'finishedTimestamp': 20,
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

    # getGameRecordRatioNumber:

    def test_getGameRecordRatioNumber_noCorrectAnswers(self):
        """
        getGameRecordRatioNumber noCorrectAnswers
        """
        print('\nRunning test', getTrace())
        record: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'winnerToken': 'player-1',
            'isWinner': True,
            'startedTimestamp': 0,
            'partnerToken': 'player-1',
            'questionAnswers': {
                # No correct answers (answers ratio is 0 -- overall ratio is 0 too)
                'Q1': 'wrong',
            },
            'finishedTimestamp': 1000,  # Any time
        }
        ratio = getGameRecordRatioNumber(record)
        self.assertEqual(ratio, 0, 'Ratio for zero number of correct answers should be 0')

    def test_getGameRecordRatioNumber_rangeForShortGames(self):
        """
        getGameRecordRatioNumber rangeForShortGames
        """
        print('\nRunning test', getTrace())
        record: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'partnerToken': 'player-1',
            'startedTimestamp': 0,
            'finishedTimestamp': 1000 * 5,  # 5 sec
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
        }
        ratio = getGameRecordRatioNumber(record)
        self.assertGreater(ratio, 1, 'Effective ratios should be positive numbers (for short games, < 10 secs)')
        self.assertLessEqual(ratio, maxRatio, 'Ratios should not exceed maxRatio (for short games, < 10 secs)')

    def test_getGameRecordRatioNumber_rangeForLongGames(self):
        """
        getGameRecordRatioNumber rangeForLongGames
        """
        print('\nRunning test', getTrace())
        record: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'partnerToken': 'player-1',
            'startedTimestamp': 0,
            'finishedTimestamp': 1000 * 60 * 20,  # 20 min
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
        }
        ratio = getGameRecordRatioNumber(record)
        self.assertGreater(ratio, 1, 'Effective ratios should be positive numbers (for long games, > 10 mins)')
        self.assertLessEqual(ratio, maxRatio, 'Ratios should not exceed maxRatio (for long games, > 10 mins)')

    def test_getGameRecordRatioNumber_rangeForExtraShortGames(self):
        """
        getGameRecordRatioNumber rangeForShortGames
        """
        print('\nRunning test', getTrace())
        record: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'partnerToken': 'player-1',
            'startedTimestamp': 0,
            'finishedTimestamp': 1,  # just msecs
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
        }
        ratio = getGameRecordRatioNumber(record)
        self.assertGreater(ratio, 1, 'Effective ratios should be positive numbers (for extra short games, < few msecs)')
        self.assertLessEqual(ratio, maxRatio, 'Ratios should not exceed maxRatio (for extra short games, < few msecs)')

    def test_getGameRecordRatioNumber_rangeForExtraLongGames(self):
        """
        getGameRecordRatioNumber rangeForLongGames
        """
        print('\nRunning test', getTrace())
        record: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'partnerToken': 'player-1',
            'startedTimestamp': 0,
            'finishedTimestamp': 1000 * 60 * 60 * 12,  # 12 hr
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
        }
        ratio = getGameRecordRatioNumber(record)
        self.assertGreater(ratio, 1, 'Effective ratios should be positive numbers (for extra long games, > few hours)')
        self.assertLessEqual(ratio, maxRatio, 'Ratios should not exceed maxRatio (for extra long games, > few hours)')

    def test_getGameRecordRatioNumber_answersPriority(self):
        """
        getGameRecordRatioNumber answersPriority
        """
        print('\nRunning test', getTrace())
        # Good time, less answers
        lessAnswers: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'startedTimestamp': 0,
            'partnerToken': 'player-1',
            'finishedTimestamp': 50 * 1000,
            'questionAnswers': {
                'Q1': 'correct',
                'Q2': 'correct',
                'Q3': 'correct',
                'Q4': 'wrong',
                'Q5': 'wrong',
            },
        }
        # Bad time, more answers
        moreAnswers: TRecordData = {  # pyright: ignore
            'gameToken': 'game-2',
            'partnerToken': 'player-2',
            'startedTimestamp': 0,
            'finishedTimestamp': 100 * 1000,
            'questionAnswers': {
                'Q1': 'correct',
                'Q2': 'correct',
                'Q3': 'correct',
                'Q4': 'correct',
                'Q5': 'correct',
            },
        }
        lessAnswersRatio = getGameRecordRatioNumber(lessAnswers)
        moreAnswersRatio = getGameRecordRatioNumber(moreAnswers)
        diff = moreAnswersRatio - lessAnswersRatio
        self.assertGreater(
            moreAnswersRatio,
            lessAnswersRatio,
            'Records with more answered questions should have greater priority')
        self.assertGreater(diff, 0, 'Records with more answered questions should have greater priority')

    # getGameRecordRatioTag

    def test_getGameRecordRatioTag_simple(self):
        """
        getGameRecordRatioTag simple
        """
        record1: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'startedTimestamp': 0,
            'partnerToken': 'player-1',
            'finishedTimestamp': 10,
            'questionAnswers': {
                'Q1': 'correct',
                # 'Q2': 'wrong',
            },
        }
        ratioTag = getGameRecordRatioTag(record1)
        self.assertTrue(ratioTag, "Should generate ratio tag")

    def test_getGameRecordRatioTag_dateAffect(self):
        """
        getGameRecordRatioTag dateAffect
        """
        print('\nRunning test', getTrace())
        record1: TRecordData = {  # pyright: ignore
            'gameToken': 'game-1',
            'startedTimestamp': 0,
            'partnerToken': 'player-1',
            'finishedTimestamp': 10,
            'questionAnswers': {
                'Q1': 'correct',
            },
        }
        record2: TRecordData = {  # pyright: ignore
            'gameToken': 'game-2',
            'partnerToken': 'player-2',
            'startedTimestamp': 10,
            'finishedTimestamp': 20,
            'questionAnswers': {
                'Q1': 'correct',
            },
        }
        ratioTag1 = getGameRecordRatioTag(record1, 0, 20)
        ratioTag2 = getGameRecordRatioTag(record2, 0, 20)
        self.assertGreater(ratioTag2, ratioTag1, 'Ratio for more actual record should be higher')

    # findMinStartedTimestamp

    def test_findMinStartedTimestamp_simple(self):
        """
        findMinStartedTimestamp simple
        """
        print('\nRunning test', getTrace())
        record1: TRecordData = {  # pyright: ignore
            'startedTimestamp': 10,
        }
        record2: TRecordData = {  # pyright: ignore
            'startedTimestamp': 1,
        }
        result = findMinStartedTimestamp([record1, record2])
        self.assertEqual(result, 1, 'Should find minimum startedTimestamp')

    # findMaxFinishedTimestamp

    def test_findMaxFinishedTimestamp_simple(self):
        """
        findMaxFinishedTimestamp simple
        """
        print('\nRunning test', getTrace())
        record1: TRecordData = {  # pyright: ignore
            'finishedTimestamp': 10,
        }
        record2: TRecordData = {  # pyright: ignore
            'finishedTimestamp': 1,
        }
        result = findMaxFinishedTimestamp([record1, record2])
        self.assertEqual(result, 10, 'Should find maximum finishedTimestamp')

    # findMaxFinishedTimestamp

    def test_findRecordsDuration_simple(self):
        """
        findRecordsDuration simple
        """
        print('\nRunning test', getTrace())
        record1: TRecordData = {  # pyright: ignore
            'startedTimestamp': 3,
            'finishedTimestamp': 10,
        }
        record2: TRecordData = {  # pyright: ignore
            'startedTimestamp': 1,
            'finishedTimestamp': 5,
        }
        result = findRecordsDuration([record1, record2])
        self.assertEqual(
            result,
            9,
            'Should find trhough-out records game duration: from first startedTimestamp to last finishedTimestamp')

    # prepareRecordsData:

    def test_prepareRecordsData_simple(self):
        """
        prepareRecordsData simple
        """
        print('\nRunning test', getTrace())
        records: List[TGameRecord] = [  # pyright: ignore
            {
                'gameToken': 'game-1',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
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
                        'finishedTimestamp': 20,
                    },
                },
            },
        ]
        results = prepareRecordsData(records)
        expectedPartnerTokens = ['player-1', 'player-2']
        partnerTokens = list(map(lambda r: r['partnerToken'], results))
        self.assertEqual(partnerTokens, expectedPartnerTokens, 'Should return records for each player')
        #  self.assertEqual(resultsSize, 2, 'Should return records for each player')

    # getSortedGameRecords:

    def test_getSortedGameRecords_simple(self):
        """
        getSortedGameRecords simple
        """
        print('\nRunning test', getTrace())
        records: List[TGameRecord] = [  # pyright: ignore
            {
                'gameToken': 'game-1',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
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
                'gameToken': 'game-2',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
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
        results = getSortedGameRecords(records, None)
        # error [Pyright reportGeneralTypeIssues] "__getitem__" method not defined on type "float"
        tokens = list(map(lambda gameRecord: gameRecord['gameToken'], results))  # pyright: ignore
        self.assertEqual(tokens, expectedTokens, 'Should return correctly sorted tokens list')

    def test_getSortedGameRecords_truncateResults(self):
        """
        getSortedGameRecords truncateResults
        """
        print('\nRunning test', getTrace())
        records: List[TGameRecord] = [  # pyright: ignore
            {
                'gameToken': 'game-1',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
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
                'gameToken': 'game-2',
                'winnerToken': 'player-1',
                'startedTimestamp': 0,
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
        results = getSortedGameRecords(records, 1)
        # error [Pyright reportGeneralTypeIssues] "__getitem__" method not defined on type "float"
        tokens = list(map(lambda gameRecord: gameRecord['gameToken'], results))  # pyright: ignore
        self.assertEqual(len(tokens), 1, 'Results should be trunctated if specified parameter `recordsTableSize`')

    #  def test_getSortedGameRecords_withDate(self):
    #      """
    #      getSortedGameRecords withDate: If have same results with different timestamps the most recent should have priority
    #      """
    #      print('\nRunning test', getTrace())
    #      records: List[TGameRecord] = [  # pyright: ignore
    #          {
    #              'gameToken': 'game-1',
    #              'winnerToken': 'player-1',
    #              'startedTimestamp': 10,
    #              'partnersInfo': {
    #                  'player-1': {
    #                      'questionAnswers': {
    #                          'Q1': 'correct',
    #                      },
    #                      'finishedTimestamp': 20,
    #                  },
    #              },
    #          },
    #          {
    #              'gameToken': 'game-2',
    #              'winnerToken': 'player-1',
    #              'startedTimestamp': 20,
    #              'partnersInfo': {
    #                  'player-2': {
    #                      'questionAnswers': {
    #                          'Q1': 'correct',
    #                      },
    #                      'finishedTimestamp': 30,
    #                  },
    #              },
    #          },
    #      ]
    #      results = getSortedGameRecords(records, 1)
    #      bestResult = results[0]
    #      bestGameToken = bestResult['gameToken']
    #      self.assertEqual(bestGameToken, 'game-2', 'Most recent records should have priority')


if __name__ == '__main__':
    DEBUG(getTrace(' test run'))
    unittest.main()
