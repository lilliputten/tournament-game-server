# -*- coding:utf-8 -*-
# @module gameHelpers
# @since 2023.03.04, 21:43
# @changed 2023.03.18, 21:19

# from typing import List, Set, Dict, Tuple, Union, TypedDict
from typing import List, Dict, Union, Callable
from functools import reduce

from config import config
# from src.core.lib.logger import DEBUG
# from src.core.lib.utils import getTrace
from src.core.lib.utils import hasNotEmpty, notEmpty
from src.core.types.RecordsTypes import TGameRecord, TRecordData, TSortedRatiosData, timestampFields


def getLatestTimestamp(list):
    max(filter(notEmpty, list))


def getGameTimestamps(gameRecord: TGameRecord) -> List[int]:
    return list(filter(None, map(lambda id: gameRecord[id] if hasNotEmpty(gameRecord, id) else None, timestampFields)))


def getLatestGameTimestamp(gameRecord: TGameRecord) -> int:
    timestamps = getGameTimestamps(gameRecord)
    return max(timestamps)


def getCorrectQuestionAnswersCount(questionAnswers: Dict) -> int:
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


def determineGameWinner(gameRecord: TGameRecord) -> Union[str, None]:
    """
    Determine game winner. Returns winned player token.
    """
    partnersInfo = gameRecord['partnersInfo']
    partners = partnersInfo.keys()  # gameRecord['partners']
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


#  maxRatio = 99999
maxRatio = 100


def findMinStartedTimestamp(records: List[TRecordData]) -> int:
    getTimestamp: Callable[[TRecordData], int] = lambda record: record['startedTimestamp']
    timestamps = map(getTimestamp, records)
    minTimestamp = min(timestamps)
    return minTimestamp


def findMaxFinishedTimestamp(records: List[TRecordData]) -> int:
    getTimestamp: Callable[[TRecordData], int] = lambda record: record['finishedTimestamp']
    timestamps = map(getTimestamp, records)
    maxTimestamp = max(timestamps)
    return maxTimestamp


def findRecordsDuration(records: List[TRecordData]) -> int:
    maxTimestamp = findMaxFinishedTimestamp(records)
    minTimestamp = findMinStartedTimestamp(records)
    return maxTimestamp - minTimestamp


# , minTimestamp: Union[int, None] = None, maxTimestamp: Union[int, None] = None) -> float:
def getGameRecordRatioNumber(recordData: TRecordData) -> float:
    """
    Calculate composite weighted game ratio (based on winner game time and answered questions number).
    The greather value means the greater priority of the record (zero means no answered questions).
    """
    # Get required data...
    # startedTimestamp = recordData['startedTimestamp']
    # finishedTimestamp = recordData['finishedTimestamp']
    questionAnswers = recordData['questionAnswers']
    totalCount = len(questionAnswers)
    correctCount = getCorrectQuestionAnswersCount(questionAnswers)
    # Time is game duration in msecs.
    # time = finishedTimestamp - startedTimestamp if finishedTimestamp is not None and startedTimestamp is not None else None
    # Calculate ratio (using extra multipliers to make ratios enought large
    # numbers: it will be divided to game time in msec and total questions
    # count)...
    ratio = 100 * correctCount  # answered questions
    if totalCount:
        ratio /= totalCount
    # if time is not None and time:
    #     timeRatio = time / 1000
    #     ratio /= timeRatio
    # DEBUG(getTrace(), {
    #     #  'winnerToken': winnerToken,
    #     #  'startedTimestamp': startedTimestamp,
    #     #  'partnersInfo': partnersInfo,
    #     #  'recordData': recordData,
    #     #  'questionAnswers': questionAnswers,
    #     #  'finishedTimestamp': finishedTimestamp,
    #     'totalCount': totalCount,
    #     'correctCount': correctCount,
    #     'time': time,
    #     'ratio': ratio,
    # })
    # # UNUSED: Trying to adjust ratio with timestamps (recent games are more prioritable)
    #  if minTimestamp is not None and maxTimestamp is not None:
    #      duration = finishedTimestamp - startedTimestamp
    #      maxDuration = maxTimestamp - minTimestamp
    #      timeRatio = duration / maxDuration
    return ratio


def getGameRecordRatioTag(recordData: TRecordData,
                          minTimestamp: Union[int,
                                              None] = None,
                          maxTimestamp: Union[int,
                                              None] = None) -> str:
    startedTimestamp = recordData['startedTimestamp']
    finishedTimestamp = recordData['finishedTimestamp']
    #  duration = finishedTimestamp - startedTimestamp
    ratio = getGameRecordRatioNumber(recordData)
    if ratio > maxRatio:
        ratio = maxRatio
    if ratio < 0:
        ratio = 0
    decimalsCount = 2
    symbolsCount = len(str(maxRatio))
    formatStr = '{:0>' + str(symbolsCount + decimalsCount + 1) + '.' + str(decimalsCount) + 'f}'
    ratioTag = formatStr.format(ratio)
    #  timestamp = recordData['finishedTimestamp']
    formatTimeStr = '{:0>13d}'
    timestampTag = formatTimeStr.format(finishedTimestamp)
    durationTag = 'NONE'
    if minTimestamp is not None and maxTimestamp is not None:
        duration = finishedTimestamp - startedTimestamp
        maxDuration = maxTimestamp - minTimestamp
        maxDurationSymbols = len(str(maxDuration))
        durationDiff = maxDuration - duration
        durationFormatStr = '{:0>' + str(maxDurationSymbols) + 'd}'
        durationTag = durationFormatStr.format(durationDiff)
        timestampTag = durationFormatStr.format(finishedTimestamp - minTimestamp)
        #  durationRatio = 100 * duration / maxDuration if maxDuration else 0
        #  durationFormatStr = '{:0>9.5f}'
        #  durationTag = durationFormatStr.format(durationRatio)
    return ratioTag + '-' + durationTag + '-' + timestampTag


def prepareRecordsData(records: List[TGameRecord]) -> List[TRecordData]:
    results: List[TRecordData] = []
    for item in records:
        winnerToken = item['winnerToken']
        partnersInfo = item['partnersInfo']
        partnersKeys = partnersInfo.keys()
        for partnerToken in partnersKeys:
            partnerData = partnersInfo[partnerToken]
            # Clone data excluding some unused keys
            newData: TRecordData = \
                dict(partnerData,
                     **{key: val for key, val in item.items()
                         if key != 'partners' and key != 'partnersInfo' and key != 'Token'})  # pyright: ignore
            newData['partnerToken'] = partnerToken
            if partnerToken == winnerToken:
                newData['isWinner'] = True
            results.append(newData)
    return results


def getSortedGameRecords(gameRecords: List[TGameRecord],
                         recordsTableSize: Union[int,
                                                 None] = config['recordsTableSize']) -> List[TRecordData]:
    """
    Get {recordsTableSize} best game records.
    """
    # Get records...
    recordsList = prepareRecordsData(gameRecords)
    minTimestamp = findMinStartedTimestamp(recordsList)
    maxTimestamp = findMaxFinishedTimestamp(recordsList)
    # Calculate ratios, remove game records with zero ratios...
    createRatiosData: Callable[[TRecordData], TSortedRatiosData] = lambda record: {
        'ratioTag': getGameRecordRatioTag(record, minTimestamp, maxTimestamp),
        'record': record,
    }
    #  ratios = list(filter(lambda r: r['ratio'] > 0, map(createRatiosData, recordsList)))
    ratios = list(map(createRatiosData, recordsList))
    # Records with a maximum ratios comes first (greater ratio = better game result)
    sortedRatios = sorted(ratios, key=lambda r: r['ratioTag'], reverse=True)
    # Truncate list if required...
    if recordsTableSize is not None and recordsTableSize < len(sortedRatios):
        del sortedRatios[recordsTableSize:]
    # Get only game records list...
    #  sortedRecords: List[Dict] = list(map(lambda r: dict(r['record']), sortedRatios))
    sortedRecords = list(map(lambda r: r['record'], sortedRatios))
    #  DEBUG(getTrace(), {
    #      'ratios': ratios,
    #      'sortedRatios': sortedRatios,
    #      # 'sortedRecords': sortedRecords,
    #      'recordsTableSize': recordsTableSize,
    #  })
    return sortedRecords


__all__ = [  # Exporting objects...
    'getGameTimestamps',
    'determineGameWinner',
    'getGameRecordRatioNumber',
    'getSortedGameRecords',
]
