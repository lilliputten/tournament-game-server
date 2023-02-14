# -*- coding:utf-8 -*-
# @module GameController
# @desc Game controller utils
# @since 2023.02.13, 13:52
# @changed 2023.02.14, 17:15


from datetime import datetime
from tinydb import Query
from tinydb.table import Document
from src import appSession
from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG, getDateStr, getMsTimeStamp
from src.core.lib.uniqueToken import createUniqueToken
from src.core.lib.utils import empty, getTrace

from src.core.Waiting import waitingStorage, WaitingConstants

# from . import GameConstants
from .GameStorage import gameStorage, GameConstants


class GameController(Storage):

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def getGameData(self, gameToken):
        # Get game data...
        q = Query()
        query = (q.Token == gameToken)
        foundGame = gameStorage.findFirstRecord(query)
        return foundGame

    def getCurrentGameData(self):
        gameToken = appSession.getVariable('gameToken')
        # Remove obsolete (timeouted) games or games with involved tokens...
        q = Query()
        query = (q.Token == gameToken)
        foundGame = gameStorage.findFirstRecord(query)
        return foundGame

    def tryStartGame(self):
        # Prepare params...
        Token = appSession.getToken()
        now = datetime.now()
        currentTimestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        currentTimeStr = getDateStr(now)

        waitingStorage.dbSync()
        gameStorage.dbSync()

        # Find first waiting partner and if found, then create a new game...
        q = Query()
        selfQuery = (q.Token == Token)
        selfRecord = waitingStorage.findFirstRecord(selfQuery)
        DEBUG(getTrace('Found selfRecord'), {
            'selfRecord': selfRecord,
            'Token': Token,
            'currentTimestamp': currentTimestamp,
            'currentTimeStr': currentTimeStr,
        })

        # Has record found?
        if not selfRecord or selfRecord is None:
            # No self record found -> error
            responseData = {
                'success': True,
                'reason': 'No self record found',
                'error': 'No waiting record found for token',
                'status': 'failed',  # waiting, finished, failed
                'Token': Token,
                'currentTimestamp': currentTimestamp,
                'currentTimeStr': currentTimeStr,
            }
            DEBUG(getTrace('No self record found -> error'), responseData)
            return responseData

        # Record already have game token?
        if 'gameToken' in selfRecord and selfRecord['gameToken'] is not None and 'partnerToken' in selfRecord and selfRecord['partnerToken'] is not None:
            # TODO: To check if it's too old token?
            # Record already have game token -> finished
            responseData = dict(selfRecord, **{
                'success': True,
                'reason': 'Record already have game token',
                'status': 'finished',  # waiting, finished, failed
                'gameTimestamp': currentTimestamp,
                'gameTimeStr': currentTimeStr,
            })
            DEBUG(getTrace('Record already have game token -> finished'), responseData)
            # Store session token to session
            appSession.setVariable('gameToken', selfRecord['gameToken'])
            appSession.setVariable('partnerToken', selfRecord['partnerToken'])
            appSession.setVariable('partnerName', selfRecord['partnerName'])  # XXX: Is it dangerous?
            return responseData

        # Check timeout...
        minimalWaitingTimestamp = currentTimestamp - WaitingConstants.validWaitingPeriodMs
        timestamp = selfRecord['timestamp']
        timestr = selfRecord['timestr']
        if timestamp < minimalWaitingTimestamp:
            # Timeout exceeded -> failed
            responseData = dict(selfRecord, **{
                'success': True,
                'reason': 'Timeout exceeded',
                'status': 'failed',  # waiting, finished, failed
                'timeDiff': timestamp - minimalWaitingTimestamp,
                'currentTimestamp': currentTimestamp,
                'currentTimeStr': currentTimeStr,
                'timestamp': timestamp,
                'timeStr': timestr,
                'minimalWaitingTimestamp': minimalWaitingTimestamp,
                'validWaitingPeriodMs': WaitingConstants.validWaitingPeriodMs,
            })
            DEBUG(getTrace('Timeout exceeded -> failed'), responseData)
            return responseData

        # Try to find partner...
        q = Query()
        #  partnerQuery = (q.Token != Token) & (~q.gameToken.exists())
        partnerQuery = (q.Token != Token) & (q.timestamp >= minimalWaitingTimestamp) & (~q.gameToken.exists())
        foundPartners = waitingStorage.findRecords(partnerQuery)
        if not len(foundPartners):
            # No partners found -> continue waiting
            responseData = dict(selfRecord, **{
                'success': True,
                'reason': 'No partners found',
                'status': 'waiting',  # waiting, finished, failed
                'currentTimestamp': currentTimestamp,
                'minimalWaitingTimestamp': minimalWaitingTimestamp,
                'validWaitingPeriodMs': WaitingConstants.validWaitingPeriodMs,
            })
            DEBUG(getTrace('No partners found -> continue waiting'), responseData)
            return responseData

        # Found partners -> start game...

        # Get partner token...
        partnerRecord = foundPartners[0]  # Choose first of found partners
        partnerToken = partnerRecord['Token']

        # Remove obsolete (timeouted) games or games with involved tokens...
        q = Query()
        query1 = (q.partners.any([Token, partnerToken]))
        minimalGameTimestamp = currentTimestamp - GameConstants.validGamePeriodMs
        query2 = (q.timestamp >= minimalGameTimestamp)
        query = (query1 | query2)
        removedGames = gameStorage.extractRecords(query)
        if len(removedGames):
            DEBUG(getTrace('Ovsolete games removed'), {
                'Token': Token,
                'partnerToken': partnerToken,
                'removedGamesCount': len(removedGames),
                'removedGames': removedGames,
                'minimalGameTimestamp': minimalGameTimestamp,
                'validGamePeriodMs': GameConstants.validGamePeriodMs,
            })

        # Prepare other params...
        partnerName = partnerRecord['name']
        selfName = selfRecord['name']
        gameToken = createUniqueToken()
        selfUpdateData = {
            'partnerToken': partnerToken,
            'partnerName': partnerName,
            'gameToken': gameToken,
        }
        partnerUpdateData = {
            'partnerToken': Token,
            'partnerName': selfName,
            'gameToken': gameToken,
        }
        gameData = {
            #  'gameToken': gameToken,
            'timestamp': currentTimestamp,
            'timestr': currentTimeStr,
            'partners': [Token, partnerToken],
            'partnersInfo': {
                Token: {
                    'name': selfName,
                },
                partnerToken: {
                    'name': partnerName,
                },
            },
        }
        # Update records...
        db = waitingStorage.getDbHandler()
        db.upsert(Document(selfUpdateData, doc_id=selfRecord.doc_id))
        db.upsert(Document(partnerUpdateData, doc_id=partnerRecord.doc_id))
        waitingStorage.dbClose()

        # Add game...
        gameRecordId = gameStorage.addRecord(Token=gameToken, data=gameData)
        gameStorage.dbSave()

        responseData = dict(selfRecord, **selfUpdateData, **{
            'success': True,
            'reason': 'Partner found, game started',
            'status': 'finished',  # waiting, finished, failed
            'gameTimestamp': currentTimestamp,
            'gameTimeStr': currentTimeStr,
            'gameRecordId': gameRecordId,
        })
        DEBUG(getTrace('Found partners -> start game'), responseData)

        # Store session token to session
        appSession.setVariable('gameToken', gameToken)
        appSession.setVariable('partnerToken', partnerToken)
        appSession.setVariable('partnerName', partnerName)  # XXX: Is it dangerous?

        return responseData

    def startGameSession(self):
        """
        It's not really a start of the game (it occured in the tryStartGame method).
        Here prepared final game data for the client.
        """
        # Prepare data...
        Token = appSession.getToken()
        gameToken = appSession.getGameToken()
        partnerToken = appSession.getVariable('partnerToken')
        partnerName = appSession.getVariable('partnerName')
        #  gameRecord = gameController.getGameData(gameToken=gameToken)

        # Empty parameters?
        if empty(Token) or empty(gameToken) or empty(partnerToken) or empty(partnerName):
            # No self record found -> error
            responseData = {
                # Params...
                'Token': Token,
                'gameToken': gameToken,
                'partnerToken': partnerToken,
                'partnerName': partnerName,

                # Status...
                'success': True,
                'status': 'failed',
                'reason': 'Error',
                'error': 'Required game parameters is not satisfied',
            }
            DEBUG(getTrace('One of required parameters is empty -> error'), responseData)
            return responseData

        responseData = {
            # Params...
            'Token': Token,
            'gameToken': gameToken,
            'partnerToken': partnerToken,
            'partnerName': partnerName,

            # Status...
            'success': True,
            'status': 'playing',
            'reason': 'Game started',
            # error?
        }

        DEBUG(getTrace('success'), responseData)
        return responseData


# Create singleton...
gameController = GameController()


__all__ = [  # Exporting objects...
    'gameController',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
