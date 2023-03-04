# -*- coding:utf-8 -*-
# @module gameHelpers
# @since 2023.03.04, 21:43
# @changed 2023.03.04, 21:43

from functools import reduce

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace


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
    partners = gameRecord['partners']
    partnersInfo = gameRecord['partnersInfo']
    startedTimestamp = gameRecord['startedTimestamp']
    maxCorrectAnswers = 0  # Maximum correct answers count
    maxCorrectTokens = []  # Collect users with that same maximum correct answers number (to find the fastest of them if there are several of them)
    stats = {}
    for tkn in partners:
        data = partnersInfo[tkn]
        questionAnswers = data['questionAnswers']
        correctAnswers = getCorrectQuestionAnswersCount(questionAnswers)
        if correctAnswers > maxCorrectAnswers:
            # New record found!
            maxCorrectAnswers = correctAnswers
            maxCorrectTokens = [tkn]
        elif  correctAnswers == maxCorrectAnswers:
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


__all__ = [  # Exporting objects...
    'determineGameWinner',
]
