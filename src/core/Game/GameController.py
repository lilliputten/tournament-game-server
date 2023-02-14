# -*- coding:utf-8 -*-
# @module GameController
# @desc Game controller utils
# @since 2023.02.13, 13:52
# @changed 2023.02.14, 21:04


from datetime import datetime
from tinydb import Query
# from tinydb.table import Document
from src import appSession
# from src.core.lib import serverUtils
from src.core.lib.Storage import Storage

from src.core.lib.logger import DEBUG, getDateStr, getMsTimeStamp
from src.core.lib.uniqueToken import createUniqueToken
from src.core.lib.utils import empty, getTrace, hasNotEmpty, notEmpty

from src.core.Waiting import WaitingHelpers, waitingStorage, WaitingConstants

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

    def doWaitingStart(self, request):
        # Get request data...
        requestData = request.json
        if not requestData:
            error = 'No parameters passed'
            responseData = {
                'success': True,
                'reason': 'Error',
                'error': error,
                'status': 'failed',  # waiting, finished, failed
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        DEBUG(getTrace('Start'), {
            'requestData': requestData,
        })

        # Get mode & store it to session...
        mode = requestData['mode']
        appSession.setVariable('mode', mode)

        # Get name & store it to session...
        if not hasNotEmpty(requestData, 'name'):
            error = 'Not specified parameter `name`!'
            responseData = {
                'success': True,
                'reason': 'Error',
                'error': error,
                'status': 'error',
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData
        name = requestData['name']
        appSession.setVariable('name', name)

        # Check mode -- waiting isn't required for 'single' mode
        if mode != 'multi':
            reason = 'No multi player mode: waiting is not required'
            responseData = dict(self.startGame(partnerRecord=None), **{
                'reason': reason,
            })
            DEBUG(getTrace(reason), responseData)
            return responseData

        # Prepare extra parameters...
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timestr = getDateStr(now)
        # Prepare data...
        data = {
            'name': name,
            'mode': mode,
            'timestamp': timestamp,
            'timestr': timestr,
            'ip': request.remote_addr,
        }
        Token = appSession.getToken()
        waitingStorage.dbSync()

        # Try to find active record
        q = Query()
        query = (q.timestamp >= timestamp - WaitingConstants.validWaitingPeriodMs) & (q.Token == Token) & (q.gameToken.exists())  # & (q.gameToken is not None)
        foundRecord = waitingStorage.findFirstRecord(query)
        DEBUG(getTrace('DEBUG findQuery'), {
            'foundRecord': foundRecord,
            #  'removedRecords': removedRecords,
        })
        # Has active game?
        if foundRecord:  # and 'gameToken' in foundRecord and not hasNotEmpty(foundRecord, 'gameToken'):
            responseData = dict(data, **{
                'success': True,
                'reason': 'Already have active game',
                'status': 'success',
                'gameToken': foundRecord['gameToken'],
                'recordId': foundRecord.doc_id,
                # error?
            })
            DEBUG(getTrace('Already have active game -> finished'), responseData)
            return responseData

        # Remove all obsolete records...
        removeQuery = WaitingHelpers.getInvalidRecordQuery(findInvalidRecords=True, Token=Token)
        removedRecords = waitingStorage.removeRecords(removeQuery)
        if len(removedRecords):
            DEBUG(getTrace('Removed records'), {
                'removedRecords': removedRecords,
                'removedRecordsCount': len(removedRecords),
            })
        #  db.upsert(Document(recordData, q.Token == Token))
        recordId = waitingStorage.addRecord(
            timestamp=timestamp,
            Token=Token,
            data=data,
        )

        # TODO: Check result of db operation?

        # Finsh & return success result...
        waitingStorage.dbClose()
        responseData = dict(data, **{
            'success': True,
            'status': 'waiting',
            'reason': 'Waiting record added. Waiting for a partner already started.',
            'recordId': recordId,
            # error?
        })
        DEBUG(getTrace('Waiting started -> waitingStarted'), responseData)
        return responseData

    def doWaitingCheck(self):
        # Prepare params...
        Token = appSession.getToken()
        now = datetime.now()
        currentTimestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        currentTimeStr = getDateStr(now)

        waitingStorage.dbSync()
        gameStorage.dbSync()

        # TODO: Check for single player game?

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
                'status': 'waitingFinished',  # waiting, finished, failed
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
        # partnerToken = partnerRecord['Token']

        responseData = self.startGame(partnerRecord)

        DEBUG(getTrace('Found partners -> start game'), responseData)
        return responseData

    def removeObsoleteGames(self, tokens):
        # Remove obsolete (timeouted) games or games with involved tokens...
        q = Query()
        query1 = (q.partners.any(tokens))
        timestamp = getMsTimeStamp(datetime.now())  # Get milliseconds timestamp (for technical usage)
        minimalGameTimestamp = timestamp - GameConstants.validGamePeriodMs
        query2 = (q.timestamp >= minimalGameTimestamp)
        query = (query1 | query2)
        removedGames = gameStorage.extractRecords(query)
        if len(removedGames):
            DEBUG(getTrace('Ovsolete games removed'), {
                'tokens': tokens,
                'removedGamesCount': len(removedGames),
                'removedGames': removedGames,
                'minimalGameTimestamp': minimalGameTimestamp,
                'validGamePeriodMs': GameConstants.validGamePeriodMs,
            })
        return len(removedGames)

    def startGame(self, partnerRecord=None):
        # Prepare params...
        Token = appSession.getToken()
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timeStr = getDateStr(now)

        # Prepare other params...
        partnerName = partnerRecord['name'] if partnerRecord else None
        partnerToken = partnerRecord['token'] if partnerRecord else None
        selfName = appSession.getVariable('name')
        mode = appSession.getVariable('mode')
        gameToken = createUniqueToken()

        partners = [Token]
        partnersInfo = {
            Token: {
                'name': selfName,
            },
        }

        # Update records...
        db = waitingStorage.getDbHandler()
        q = Query()

        # Update own record...
        selfUpdateData = {
            'partnerToken': partnerToken,
            'partnerName': partnerName,
            'gameToken': gameToken,
        }
        db.update(selfUpdateData, q.Token == Token)  # doc_id=selfRecord.doc_id))

        # Update partner' record...
        if notEmpty(partnerToken):
            partners.append(partnerToken)
            partnersInfo[partnerToken] = {
                'name': partnerName,
            }
            partnerUpdateData = {
                'partnerToken': Token,
                'partnerName': selfName,
                'gameToken': gameToken,
            }
            db.update(partnerUpdateData, (q.Token == partnerToken))  # doc_id=partnerRecord.doc_id))

        # Close waiting storage
        waitingStorage.dbSave()

        # Add game record...
        gameData = {
            'gameToken': gameToken,
            'gameMode': mode,
            'timestamp': timestamp,
            'timestr': timeStr,
            'partners': partners,
            'partnersInfo': partnersInfo,
        }

        # Remove old game records...
        self.removeObsoleteGames(partners)

        # Add game
        gameRecordId = gameStorage.addRecord(Token=gameToken, data=gameData)
        gameStorage.dbSave()

        # Update session...
        appSession.setVariable('gameToken', gameToken)
        appSession.setVariable('partnerToken', partnerToken)
        appSession.setVariable('partnerName', partnerName)  # XXX: Is it dangerous?

        # Return data...
        responseData = dict(**selfUpdateData, **{
            'success': True,
            'reason': 'Game started',
            'status': 'waitingFinished',  # waiting, finished, failed
            'gameMode': mode,
            'gameTimestamp': timestamp,
            'gameTimeStr': timeStr,
            'gameRecordId': gameRecordId,
        })
        DEBUG(getTrace('Game started'), responseData)
        return responseData

    def startGameSession(self):
        """
        It's not really a start of the game (it occured in the doWaitingCheck method).
        Here prepared final game data for the client.
        """
        # Prepare data...
        Token = appSession.getToken()
        gameToken = appSession.getGameToken()
        gameMode = appSession.getVariable('mode')
        partnerToken = appSession.getVariable('partnerToken')
        partnerName = appSession.getVariable('partnerName')
        #  gameRecord = gameController.getGameData(gameToken=gameToken)

        # Empty parameters?
        if empty(Token) or empty(gameToken) or (gameMode == 'multi' and empty(partnerToken)):
            # No self record found -> error
            responseData = {
                # Params...
                'Token': Token,
                'gameToken': gameToken,
                'gameMode': gameMode,
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
            'gameMode': gameMode,
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
