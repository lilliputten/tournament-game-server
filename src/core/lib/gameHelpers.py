# -*- coding:utf-8 -*-
# @module gameHelpers
# @since 2023.03.04, 21:43
# @changed 2023.03.05, 23:43

from functools import reduce
# import random

from config import config
# from src.core.lib.logger import DEBUG
# from src.core.lib.utils import getTrace
from src.core.lib.utils import hasNotEmpty, notEmpty


def getLatestTimestamp(list):
    max(filter(notEmpty, list))


def getGameTimestamps(gameRecord):
    ids = ['timestamp', 'startedTimestamp', 'lastActivityTimestamp']
    return list(filter(None, map(lambda id: gameRecord[id] if hasNotEmpty(gameRecord, id) else None, ids)))


def getLatestGameTimestamp(gameRecord):
    timestamps = getGameTimestamps(gameRecord)
    return max(timestamps)


def getCorrectQuestionAnswersCount(questionAnswers):
    count = reduce(lambda count, key: count + 1 if questionAnswers[key] == 'correct' else count, questionAnswers, 0)
    return count


def findQuckestWinnerByStats(stats):
    minTime = None
    minToken = None
    for tkn in stats:
        item = stats[tkn]
        time = item['time']
        if minTime is None or time < minTime:
            minTime = time
            minToken = tkn
    return minToken


def determineGameWinner(gameRecord):
    """
    Determine game winner. Returns winned player token.
    """
    partners = gameRecord['partners']
    partnersInfo = gameRecord['partnersInfo']
    startedTimestamp = gameRecord['startedTimestamp']
    maxCorrectAnswers = 0  # Maximum correct answers count
    # Collect users with that same maximum correct answers number (to find the
    # fastest of them if there are several of them)
    maxCorrectTokens = []
    stats = {}
    for tkn in partners:
        data = partnersInfo[tkn]
        questionAnswers = data['questionAnswers']
        correctAnswers = getCorrectQuestionAnswersCount(questionAnswers)
        if correctAnswers > maxCorrectAnswers:
            # New record found!
            maxCorrectAnswers = correctAnswers
            maxCorrectTokens = [tkn]
        elif correctAnswers == maxCorrectAnswers:
            # Add this user to winner pretenders list
            maxCorrectTokens.append(tkn)
        finishedTimestamp = data['finishedTimestamp']
        time = finishedTimestamp - startedTimestamp
        stats[tkn] = {
            'Token': tkn,
            'correctAnswers': correctAnswers,
            'time': time,
        }
    maxCorrectTokensCount = len(maxCorrectTokens)
    #  DEBUG(getTrace('stats'), {
    #      'partners': partners,
    #      'partnersInfo': partnersInfo,
    #      'stats': stats,
    #      'maxCorrectTokens': maxCorrectTokens,
    #      'maxCorrectAnswers': maxCorrectAnswers,
    #      'maxCorrectTokensCount': maxCorrectTokensCount,
    #  })
    if maxCorrectTokensCount == 0:
        # No winners found!
        return None
    elif maxCorrectTokensCount == 1:
        # Only winner found!
        return maxCorrectTokens[0]
    # Found several winners: Trying to find the fastest user...
    fastestToken = findQuckestWinnerByStats(stats)
    #  DEBUG(getTrace('fastestToken'), {
    #      'fastestToken': fastestToken,
    #      'partners': partners,
    #      'partnersInfo': partnersInfo,
    #      'stats': stats,
    #      'maxCorrectTokens': maxCorrectTokens,
    #      'maxCorrectAnswers': maxCorrectAnswers,
    #      'maxCorrectTokensCount': maxCorrectTokensCount,
    #  })
    return fastestToken


def getGameRecordRatio(gameRecord):
    """
    Calculate composite weighted game ratio (based on winner game time and answered questions number).
    """
    # Get required data...
    winnerToken = gameRecord['winnerToken']
    startedTimestamp = gameRecord['startedTimestamp']
    partnersInfo = gameRecord['partnersInfo']
    info = partnersInfo[winnerToken]
    # TODO: Check for: not empty info?
    questionAnswers = info['questionAnswers']
    finishedTimestamp = info['finishedTimestamp']
    totalCount = len(questionAnswers)
    correctCount = getCorrectQuestionAnswersCount(questionAnswers)
    # Time is game duration in msecs.
    time = finishedTimestamp - startedTimestamp if finishedTimestamp is not None and startedTimestamp is not None else None
    # Calculate ratio (using extra multipliers to make ratios enought large numbers: it will be divided to game time in msec and total questions count)...
    ratio = 1000 * correctCount
    if totalCount:
        ratio /= totalCount
    if time is not None and time:
        ratio /= time / 60000
    #  DEBUG(getTrace(), {
    #      #  'winnerToken': winnerToken,
    #      #  'startedTimestamp': startedTimestamp,
    #      #  'partnersInfo': partnersInfo,
    #      #  'info': info,
    #      #  'questionAnswers': questionAnswers,
    #      #  'finishedTimestamp': finishedTimestamp,
    #      'totalCount': totalCount,
    #      'correctCount': correctCount,
    #      'time': time,
    #      'ratio': ratio,
    #  })
    return ratio


def getFirstSortedGameRecords(records, recordsTableSize=config['recordsTableSize']):
    """
    Get {recordsTableSize} best game records.
    """
    # Calculate ratios, remove game records with zero ratios...
    ratios = filter(lambda r: r['ratio'] > 0, map(lambda gameRecord: {
        'ratio': getGameRecordRatio(gameRecord),
        'gameRecord': gameRecord,
    }, records))
    # Records with a maximum ratios comes first (largest ration = better game result)
    sortedRatios = sorted(ratios, key=lambda r: r['ratio'], reverse=True)
    # Truncate list if required...
    if recordsTableSize is not None and recordsTableSize < len(sortedRatios):
        del sortedRatios[recordsTableSize:]
    # Get only game records list...
    sortedRecords = list(map(lambda r: r['gameRecord'], sortedRatios))
    #  DEBUG(getTrace(), {
    #      'ratios': ratios,
    #      'sortedRatios': sortedRatios,
    #      # 'sortedRecords': sortedRecords,
    #      'recordsTableSize': recordsTableSize,
    #  })
    return sortedRecords


def getSortedGameRecordTokens(records, recordsTableSize=config['recordsTableSize']):
    """
    Git {recordsTableSize} best game tokens (used for tests only?).
    """
    sortedRecords = getFirstSortedGameRecords(records, recordsTableSize)
    tokens = list(map(lambda gameRecord: gameRecord['Token'], sortedRecords))
    return tokens


__all__ = [  # Exporting objects...
    'getGameTimestamps',
    'determineGameWinner',
    'getGameRecordRatio',
    'getFirstSortedGameRecords',
    'getSortedGameRecordTokens',
]
