# -*- coding:utf-8 -*-
# @module gameHelpers
# @since 2023.03.18, 20:27
# @changed 2023.03.18, 20:27


from typing import List, Dict, TypedDict

# @see https://peps.python.org/pep-0589/


timestampFields: List[str] = [
    'timestamp',
    'finishedTimestamp',
    'lastAnswerTimestamp',
    'lastCheckTimestamp',
    'startedTimestamp',
]


class TPartnerInfo(TypedDict):
    finishedTimestamp: int
    finishedTimestr: str
    name: str
    questionAnswers: Dict[str, str]
    status: str


class TGameRecord(TypedDict):
    Token: str
    finishedByPartner: str
    finishedStatus: str
    finishedTimestamp: int
    finishedTimestr: str
    gameMode: str
    gameStatus: str
    gameToken: str
    lastAnswerTimestamp: int
    lastAnswerTimestr: str
    lastAnsweredBy: str
    lastCheckTimestamp: int
    lastCheckTimestr: str
    lastCheckedBy: str
    partners: List[str]
    partnersInfo: Dict[str, TPartnerInfo]
    questionsIds: List[str]
    startedTimestamp: int
    startedTimestr: str
    timestamp: int
    timestr: str
    winnerToken: str


class TRecordData(TypedDict):
    partnerToken: str
    isWinner: bool
    finishedByPartner: str
    finishedStatus: str
    finishedTimestamp: int
    finishedTimestr: str
    gameMode: str
    gameStatus: str
    gameToken: str
    lastAnswerTimestamp: int
    lastAnswerTimestr: str
    lastAnsweredBy: str
    lastCheckTimestamp: int
    lastCheckTimestr: str
    lastCheckedBy: str
    questionsIds: List[str]
    startedTimestamp: int
    startedTimestr: str
    timestamp: int
    timestr: str
    winnerToken: str
    finishedTimestamp: int
    finishedTimestr: str
    name: str
    questionAnswers: Dict[str, str]  # TODO?
    status: str


class TSortedRatiosData(TypedDict):
    #  ratio: float
    ratioTag: str
    record: TRecordData


__all__ = [  # Exporting objects...
    'TPartnerInfo',
    'TGameRecord',
    'TRecordData',
    'TSortedRatiosData',
]
