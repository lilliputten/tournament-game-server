# -*- coding:utf-8 -*-
# @module GameController
# @desc Game controller utils
# @since 2023.02.13, 13:52
# @changed 2023.03.05, 05:26


from datetime import datetime
from tinydb import Query
# from tinydb.table import Document
from src import appSession
from src.core.Questions import questions
from src.core.Records import recordsStorage
# from src.core.lib import serverUtils
from src.core.lib.Storage import Storage
from functools import reduce

from src.core.lib.logger import DEBUG, getDateStr, getMsTimeStamp
from src.core.lib.uniqueToken import createUniqueToken
from src.core.lib.utils import empty, getObjKey, getTrace, hasNotEmpty, notEmpty

from src.core.Waiting import WaitingHelpers, waitingStorage, WaitingConstants

from .GameStorage import gameStorage, GameConstants

from src.core.lib.gameHelpers import determineGameWinner


class GameController(Storage):

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def getGameData(self, gameToken):
        # TODO: Remove obsolete (timeouted) games or games with involved tokens?
        # Get game data...
        q = Query()
        # TODO: Lookup for active games only?
        foundGame = gameStorage.findFirstRecord(q.Token == gameToken)
        return foundGame

    def getCurrentGameData(self):
        gameToken = appSession.getVariable('gameToken')
        return self.getGameData(gameToken=gameToken)

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
        gameMode = requestData['gameMode']
        appSession.setVariable('gameMode', gameMode)

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
        if gameMode != 'multi':
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
            'gameMode': gameMode,
            'timestamp': timestamp,
            'timestr': timestr,
            'ip': request.remote_addr,
        }
        Token = appSession.getToken()

        waitingStorage.dbSync()

        # Try to find active waiting record
        q = Query()
        query = (
            q.timestamp >= timestamp -
            WaitingConstants.validWaitingPeriodMs) & (
            q.Token == Token) & (
            q.gameToken.exists())  # & (q.gameToken is not None)
        foundRecord = waitingStorage.findFirstRecord(query)
        DEBUG(getTrace('DEBUG findQuery'), {
            'foundRecord': foundRecord,
            #  'removedRecords': removedRecords,
        })
        # Has active game?
        if foundRecord:  # and 'gameToken' in foundRecord and not hasNotEmpty(foundRecord, 'gameToken'):
            gameToken = getObjKey(foundRecord, 'gameToken')
            partnerName = getObjKey(foundRecord, 'partnerName')
            partnerToken = getObjKey(foundRecord, 'partnerToken')

            # TODO: Check active game record?
            gameStorage.dbSync()

            q = Query()
            query = (q.gameToken == gameToken) & ((q.gameStatus == 'waiting') | (q.gameStatus == 'active'))
            gameRecord = gameStorage.findFirstRecord(query)

            #  if gameRecord:
            responseData = dict(gameRecord if gameRecord else {}, **data, **{
                'Token': Token,
                'success': True,
                'reason': 'Already have active game',
                'status': 'waitingFinished',
                #  'gameToken': gameToken,
                #  'gameMode': gameMode,
                'gameResumed': True if gameRecord else False,
                'partnerName': partnerName,
                'partnerToken': partnerToken,
                'recordId': foundRecord.doc_id,
                # error?
            })
            appSession.setVariable('gameToken', gameToken)
            appSession.setVariable('gameMode', gameMode)
            appSession.setVariable('partnerName', partnerName)
            appSession.setVariable('partnerToken', partnerToken)
            # TODO: Update game timesamp?
            DEBUG(getTrace('Already have active game -> finished (game starting)'), responseData)
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
        reason = 'Waiting record added. Waiting for a partner already started.'
        responseData = dict(data, **{
            'success': True,
            'status': 'waiting',
            'reason': reason,
            'recordId': recordId,
            # error?
        })
        DEBUG(getTrace(reason), responseData)
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
            # TODO: Update game timestamp?
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

        # Start game...
        responseData = self.startGame(partnerRecord)

        DEBUG(getTrace('Found partners -> start game'), responseData)
        return responseData

    def removeAllObsoleteGames(self):
        # Remove obsolete (timeouted) games or games with involved tokens...
        q = Query()
        timestamp = getMsTimeStamp(datetime.now())  # Get milliseconds timestamp (for technical usage)
        minimalTimestamp = timestamp - GameConstants.storeOldGamePeriodMs
        query = q.timestamp <= minimalTimestamp
        # query = query & (q.gameStatus != 'finished')  # Preserve finished games
        # (TODO: stopped?) TODO: Remove inactive (active=False) games?
        removedGames = gameStorage.extractRecords(query)
        if len(removedGames):
            DEBUG(getTrace('Ovsolete games removed'), {
                'removedGamesCount': len(removedGames),
                'removedGames': removedGames,
                'minimalTimestamp': minimalTimestamp,
                'storeOldGamePeriodMs': GameConstants.storeOldGamePeriodMs,
                'first game diff': minimalTimestamp - removedGames[0]['timestamp']
            })
        return len(removedGames)

    def removeObsoleteWaitingGamesForPartners(self, tokens=None):
        # Remove obsolete (timeouted) games or games with involved tokens...
        q = Query()
        timestamp = getMsTimeStamp(datetime.now())  # Get milliseconds timestamp (for technical usage)
        minimalTimestamp = timestamp - GameConstants.validWaitingGamePeriodMs
        query = q.timestamp <= minimalTimestamp
        # query = q.timestamp >= minimalTimestamp # Is it correct?
        if tokens and tokens is not None:
            query = query | q.partners.any(tokens)
        # Preserve finished games (TODO: stopped?) TODO: Remove inactive (active=False) games?
        query = query & (q.gameStatus != 'finished')
        removedGames = gameStorage.extractRecords(query)
        if len(removedGames):
            DEBUG(getTrace('Ovsolete games removed'), {
                'tokens': tokens,
                'removedGamesCount': len(removedGames),
                'removedGames': removedGames,
                'minimalTimestamp': minimalTimestamp,
                'validWaitingGamePeriodMs': GameConstants.validWaitingGamePeriodMs,
                'first game diff': minimalTimestamp - removedGames[0]['timestamp']
            })
        return len(removedGames)

    def createRandomQuestionIdsList(self):
        list = questions.getClientQuestionIdsList()
        return list

    def startGame(self, partnerRecord=None):
        # Prepare params...
        Token = appSession.getToken()
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timeStr = getDateStr(now)

        # Prepare other params...
        partnerName = partnerRecord['name'] if partnerRecord else None
        partnerToken = partnerRecord['Token'] if partnerRecord else None
        selfName = appSession.getVariable('name')
        gameMode = appSession.getVariable('gameMode')
        gameToken = createUniqueToken()

        partners = [Token]
        partnersInfo = {
            Token: {
                'name': selfName,
                'questionAnswers': {},
                'status': 'playing',
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
                'questionAnswers': {},
                'status': 'playing',
            }
            partnerUpdateData = {
                'partnerToken': Token,
                'partnerName': selfName,
                'gameToken': gameToken,
            }
            db.update(partnerUpdateData, (q.Token == partnerToken))  # doc_id=partnerRecord.doc_id))

        # Close waiting storage
        waitingStorage.dbSave()

        # Prepare questions list
        questionsIds = self.createRandomQuestionIdsList()

        # Add game record...
        gameData = {
            'questionsIds': questionsIds,
            'gameStatus': 'active',
            # 'lastActivityTimestamp': timestamp,
            # 'lastActivityTimestr': timeStr,
            'gameToken': gameToken,
            'gameMode': gameMode,
            'startedTimestamp': timestamp,
            'startedTimestr': timeStr,
            'timestamp': timestamp,  # Last activity!
            'timestr': timeStr,  # Last activity!
            'partners': partners,
            'partnersInfo': partnersInfo,
        }

        # Remove old game records...
        # NOTE: Removing all old games, not only for current players!
        self.removeObsoleteWaitingGamesForPartners(partners)
        self.removeAllObsoleteGames()

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
            'gameMode': gameMode,
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
        gameMode = appSession.getVariable('gameMode')
        partnerToken = appSession.getVariable('partnerToken')
        partnerName = appSession.getVariable('partnerName')

        # Empty parameters?
        if not gameToken or empty(gameToken) or (gameMode == 'multi' and empty(partnerToken)):
            error = 'Required game parameters is not satisfied'
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
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        gameStorage.dbSync()

        # Check if game is active
        gameRecord = self.getGameData(gameToken=gameToken)
        if not gameRecord:
            error = 'No game record found for gameToken ' + gameToken
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData
        gameStatus = gameRecord['gameStatus']
        if gameStatus != 'active':
            error = 'Game is not active (' + gameStatus + ')'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        # Echo game data
        responseData = dict(gameRecord, **{
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
        })

        DEBUG(getTrace('success'), responseData)
        return responseData

    def gameSessionStop(self):
        """
        Try to stop game.
        """
        # Prepare data...
        Token = appSession.getToken()
        gameToken = appSession.getGameToken()
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timestr = getDateStr(now)

        gameStorage.dbSync()

        if not gameToken:
            error = 'No game token passed'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        q = Query()
        query = (q.Token == gameToken)  # & (q.gameStatus == 'active')
        gameRecord = gameStorage.findFirstRecord(query)

        if not gameRecord:
            error = 'No game record found for token ' + gameToken
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        gameStatus = gameRecord['gameStatus']
        if gameStatus != 'active':
            error = 'Game is not active (' + gameStatus + ')'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        db = gameStorage.getDbHandler()

        # Update own record...
        gameStatus = 'stopped'
        gameUpdateData = {
            'gameStatus': gameStatus,
            'stoppedByPartner': Token,
            'timestamp': timestamp,
            'timestr': timestr,
            'stoppedTimestamp': timestamp,
            'stoppedTimestr': timestr,
            # TODO: Update partnersInfo data?
        }
        db.update(gameUpdateData, query)  # doc_id=selfRecord.doc_id))

        gameStorage.dbSave()

        # Remove game waitings for this game
        q = Query()
        query = (q.gameToken.exists()) & (q.gameToken == gameToken)
        removedWaitings = waitingStorage.extractRecords(query)

        waitingStorage.dbSave()

        # # Update session (!!!)
        # appSession.removeVariable('gameToken')
        # appSession.removeVariable('gameMode')
        # appSession.removeVariable('partnerName')
        # appSession.removeVariable('partnerToken')

        reason = 'Game stopped'
        responseData = dict(gameRecord, **gameUpdateData, **{
            'Token': Token,
            'gameToken': gameToken,
            'gameStatus': gameStatus,
            'success': True,
            'status': 'gameStopped',
            'reason': reason,
            # error?
        })
        DEBUG(getTrace(reason), dict(responseData, **{
            'removedWaitings': removedWaitings,
        }))
        return responseData

    def gameSessionFinished(self):
        """
        Try to finish game.
        """
        # Prepare data...
        Token = appSession.getToken()
        gameToken = appSession.getGameToken()
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timestr = getDateStr(now)

        gameStorage.dbSync()

        if not gameToken:
            error = 'No game token passed'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        q = Query()
        query = (q.Token == gameToken)  # & (q.gameStatus == 'active')
        gameRecord = gameStorage.findFirstRecord(query)

        if not gameRecord:
            error = 'No game record found for token ' + gameToken
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        oldGameStatus = gameRecord['gameStatus']
        oldFinishedStatus = gameRecord['finishedStatus'] if 'finishedStatus' in gameRecord else 'none'
        # correctStatus = gameStatus == 'active' or (gameStatus == 'finished' and finishedStatus != 'allFinished')
        # if not correctStatus:
        #     error = 'Invalid game status (gameStatus: ' + gameStatus + ', finishedStatus: ' + finishedStatus + ')'
        #     responseData = {
        #         'success': False,
        #         'reason': 'Error',
        #         'error': error,
        #         'gameStatus': gameStatus,
        #         'finishedStatus': finishedStatus,
        #     }
        #     DEBUG(getTrace('Error: ' + error), responseData)
        #     return responseData

        partners = gameRecord['partners']
        partnersInfo = gameRecord['partnersInfo']
        selfInfo = partnersInfo[Token]
        selfInfo['status'] = 'finished'
        selfInfo['finishedTimestamp'] = timestamp
        selfInfo['finishedTimestr'] = timestr
        partnersInfo[Token] = selfInfo
        gameRecord['partnersInfo'] = partnersInfo

        # gameStatus = 'finished'
        # finishedStatus = oldFinishedStatus

        db = gameStorage.getDbHandler()

        # Update own record...
        gameStatus = 'finished'
        isAll = reduce(lambda status, tkn: status and partnersInfo[tkn]['status'] == 'finished', partners, True)
        finishedStatus = 'all' if isAll else 'some'
        winnerToken = determineGameWinner(gameRecord) if isAll else None
        gameUpdateData = {
            'gameStatus': gameStatus,
            'winnerToken': winnerToken,
            'finishedStatus': finishedStatus,
            'finishedByPartner': Token,
            'timestamp': timestamp,
            'timestr': timestr,
            'finishedTimestamp': timestamp,
            'finishedTimestr': timestr,
        }
        db.update(gameUpdateData, query)

        # Remove old games...
        q = Query()
        query = ((
            q.timestamp < timestamp -
            GameConstants.storeOldGamePeriodMs) & ((
                q.gameMode == 'finished') | (
                q.gameMode == 'stopped')))  # & (q.gameToken is not None)
        removedGames = gameStorage.extractRecords(query)
        removedGamesCount = len(removedGames)
        if removedGamesCount:
            DEBUG(getTrace('Removed old games'), {
                'removedGamesCount': removedGamesCount,
                'removedGames': removedGames,
            })

        gameStorage.dbSave()

        if isAll:
            # Save game record data
            updatedGameRecord = dict(gameRecord, **gameUpdateData)
            DEBUG(getTrace('Save game record data'), updatedGameRecord)
            recordsStorage.dbSync()
            recordsStorage.addRecord(Token=gameToken, data=updatedGameRecord)
            recordsStorage.dbSave()
            # TODO: Remove from active games? (Or leave it there -- and it'll be removed later automatcally?)

        # Remove game waitings for this game
        q = Query()
        query = (q.gameToken.exists()) & (q.gameToken == gameToken)
        removedWaitings = waitingStorage.extractRecords(query)

        waitingStorage.dbSave()

        reason = 'Game finished'
        responseData = dict(gameRecord, **gameUpdateData, **{
            'Token': Token,
            'gameToken': gameToken,
            'oldFinishedStatus': oldFinishedStatus,
            'oldGameStatus': oldGameStatus,
            #  'gameStatus': gameStatus,
            'success': True,
            'status': 'gameFinished',
            'reason': reason,
            #  'startedTimestamp': gameRecord['startedTimestamp'],
            #  'startedTimestr': gameRecord['startedTimestr'],
            #  'finishedTimestamp': timestamp,
            #  'finishedTimestr': timestr,
            # error?
        })
        DEBUG(getTrace(reason), dict(responseData, **{
            'removedWaitings': removedWaitings,
        }))
        return responseData

    def doCheckAnswer(self, request):
        # Prepare extra parameters...
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timestr = getDateStr(now)

        Token = appSession.getToken()
        gameToken = appSession.getVariable('gameToken')

        # Get request data...
        requestData = request.json
        if not requestData:
            error = 'No parameters passed'
            responseData = {
                'success': True,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        # Check params...
        if not hasNotEmpty(requestData, 'questionId'):
            error = 'Not specified parameter `questionId`!'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData
        if not hasNotEmpty(requestData, 'answerId'):
            error = 'Not specified parameter `answerId`!'
            responseData = {
                'success': False,
                'reason': 'Error',
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        # Get params...
        questionId = requestData['questionId']
        answerId = requestData['answerId']

        questionsData = questions.getQuestionsData()
        questionsList = questionsData['questions']

        foundQuestions = list(filter(lambda q: q['id'] == questionId, questionsList))
        question = foundQuestions[0] if foundQuestions else None
        #  question = list(filter(lambda q: q['id'] == questionId, questionsList))
        foundAnswers = list(filter(lambda a: a['id'] == answerId,
                                   question['answers'])) if question and 'answers' in question else None
        answer = foundAnswers[0] if foundAnswers else None

        isCorrect = True if answer and 'correct' in answer and answer['correct'] else False

        #  DEBUG(getTrace('Start'), {
        #      'isCorrect': isCorrect,
        #      'questionId': questionId,
        #      'answerId': answerId,
        #      'requestData': requestData,
        #      'questionsList': questionsList,
        #      'question': question,
        #      'answer': answer,
        #  })

        # Get game data...
        gameStorage.dbSync()
        q = Query()
        gameQuery = q.Token == gameToken
        gameRecord = gameStorage.findFirstRecord(gameQuery)
        if not gameRecord:
            error = 'Not found game record for game token ' + gameToken
            responseData = {
                'success': False,
                'reason': 'Error',
                'status': 'noGame',
                'gameToken': gameToken,
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        # Get questionAnswers
        partnersInfo = gameRecord['partnersInfo']
        selfInfo = partnersInfo[Token]
        questionAnswers = selfInfo['questionAnswers'] if hasNotEmpty(selfInfo, 'questionAnswers') else {}
        # Update current question answer
        questionAnswers[questionId] = 'correct' if isCorrect else 'wrong'
        # Update data in game record
        selfInfo['questionAnswers'] = questionAnswers
        partnersInfo[Token] = selfInfo
        gameRecord['partnersInfo'] = partnersInfo

        #  DEBUG(getTrace('gameRecord'), {
        #      'Token': Token,
        #      'gameToken': gameToken,
        #      'gameRecord': gameRecord,
        #      'partnersInfo': partnersInfo,
        #  })

        # Prepare game data to update...
        gameUpdateData = {
            'timestamp': timestamp,
            'timestr': timestr,
            'lastAnswerTimestamp': timestamp,
            'lastAnswerTimestr': timestr,
            'lastAnsweredBy': Token,
            # Update game state (questionIdx in partnersInfo
            'partnersInfo': partnersInfo,
        }

        # Update game data...
        db = gameStorage.getDbHandler()
        db.update(gameUpdateData, gameQuery)
        gameStorage.dbSave()

        # Prepare response data...
        data = {
            #  'timestamp': timestamp,
            #  'timestr': timestr,
            'questionId': questionId,
            'answerId': answerId,
            # 'question': question, # Do not expose full data (contains `correct` fields)
            'answer': answer,
            'isCorrect': isCorrect,
            'partnersInfo': partnersInfo,
            'questionAnswers': questionAnswers,
        }

        reason = 'Answer checked'
        responseData = dict(gameRecord, **data, **{
            'Token': Token,
            'gameToken': gameToken,
            'success': True,
            #  'status': 'debug',
            'reason': reason,
        })
        DEBUG(getTrace(reason), responseData)
        return responseData

    def doSessionCheck(self, request):
        # Prepare extra parameters...
        now = datetime.now()
        timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        timestr = getDateStr(now)

        Token = appSession.getToken()
        gameToken = appSession.getVariable('gameToken')

        # Get game data...
        gameStorage.dbSync()
        q = Query()
        gameQuery = q.Token == gameToken
        gameRecord = gameStorage.findFirstRecord(gameQuery)

        # Has game record found?
        if not gameRecord:
            error = 'Not found game record for game token ' + gameToken
            responseData = {
                'success': False,
                'reason': 'Error',
                'status': 'noGame',
                'gameToken': gameToken,
                'error': error,
            }
            DEBUG(getTrace('Error: ' + error), responseData)
            return responseData

        # # Check game status...
        # gameStatus = gameRecord['gameStatus']
        # if gameStatus != 'active':
        #     error = 'Game is not active (' + gameStatus + ')'
        #     responseData = {
        #         'success': False,
        #         'reason': 'Error',
        #         'status': 'gameNotActive',
        #         'gameStatus': gameStatus,
        #         'error': error,
        #     }
        #     DEBUG(getTrace('Error: ' + error), responseData)
        #     return responseData

        # Get partnersInfo & questionAnswers...
        partnersInfo = gameRecord['partnersInfo']
        selfInfo = partnersInfo[Token]
        questionAnswers = selfInfo['questionAnswers'] if hasNotEmpty(selfInfo, 'questionAnswers') else {}

        DEBUG(getTrace('gameRecord'), {
            'Token': Token,  # TODO: Token is gameToken?
            'gameToken': gameToken,
            'gameRecord': gameRecord,
            'partnersInfo': partnersInfo,
        })

        # Prepare game data to update (timestamps & check info)...
        gameUpdateData = {
            'timestamp': timestamp,
            'timestr': timestr,
            'lastCheckTimestamp': timestamp,
            'lastCheckTimestr': timestr,
            'lastCheckedBy': Token,
        }

        # Update game data...
        db = gameStorage.getDbHandler()
        db.update(gameUpdateData, gameQuery)
        gameStorage.dbSave()

        # Prepare response data...
        data = {
            'Token': Token,
            #  'gameToken': gameToken,
            #  'gameStatus': gameStatus,
            'partnersInfo': partnersInfo,
            'questionAnswers': questionAnswers,
        }

        reason = 'Game status checked'
        responseData = dict(gameRecord, **data, **{
            'success': True,
            'status': 'gameStatusResult',
            'reason': reason,
        })
        DEBUG(getTrace(reason), responseData)
        return responseData


# Create singleton...
gameController = GameController()


__all__ = [  # Exporting objects...
    'gameController',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
