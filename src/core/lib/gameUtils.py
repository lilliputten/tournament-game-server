
from src.core.lib.utils import hasNotEmpty, notEmpty


def getLatestTimestamp(list):
    max(filter(notEmpty, list))


def getGameTimestamps(gameRecord):
    ids = ['timestamp', 'startedTimestamp', 'lastActivityTimestamp']
    return list(filter(None, map(lambda id: gameRecord[id] if hasNotEmpty(gameRecord, id) else None, ids)))


def getLatestGameTimestamp(gameRecord):
    timestamps = getGameTimestamps(gameRecord)
    return max(timestamps)


__all__ = [  # Exporting objects...
    'getGameTimestamps',
]
