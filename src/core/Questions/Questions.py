# -*- coding:utf-8 -*-
# @module Questions
# @desc Questions...
# @since 2023.02.15, 01:48
# @changed 2023.03.04, 18:40

from os import path
import yaml
from datetime import datetime
from random import random
import math

from config import config

from src.core.lib.logger import DEBUG, getMsTimeStamp
from src.core.lib.utils import empty, getTrace, hasNotEmpty


class Questions():

    testMode = None
    questionsData = None
    loadTimestamp = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def getFileName(self):
        rootPath = config['rootPath']
        # TODO: To move source file names to config?
        #  if config['isDev']:  # Only debug mode, TODO: To check for `useSampleQuestions` parameter?
        #      file = path.join(rootPath, 'questions.SAMPLE.yaml')
        #      if path.isfile(file):
        #          return file
        file = path.join(rootPath, 'questions.yaml')
        if path.isfile(file):
            return file
        file = path.join(rootPath, 'questions.default.yaml')
        if path.isfile(file):
            return file
        return None

    def loadQuestionsData(self):
        file = self.getFileName()
        if file and path.isfile(file):
            with open(file, encoding='UTF-8') as handler:
                return yaml.load(handler, Loader=yaml.FullLoader)
        return {}

    def getOrLoadQuestionsData(self, forceLoad=False):
        questionsData = self.questionsData
        timestamp = getMsTimeStamp(datetime.now())
        validTimestamp = timestamp - config['validQuestionsPeriodMs']
        # NOTE: Updating question once in validQuestionsPeriodMs period
        if empty(self.loadTimestamp) or self.loadTimestamp < validTimestamp:
            forceLoad = True
        if questionsData is None or forceLoad:
            questionsData = self.loadQuestionsData()
            questionsData = dict(questionsData,
                                 **{'questions': self.ensureQuestionsAndAnswersIds(questionsData['questions'])})
            self.questionsData = questionsData
            self.loadTimestamp = timestamp
        return questionsData

    def ensureQuestionAnswersIds(self, q):
        answers = q['answers']
        resultedAnswers = [dict(a, **{'id': a['id'] if hasNotEmpty(a, 'id') else 'A' + str(i + 1)})
                           for i, a in enumerate(answers)]
        return dict(q, **{'answers': resultedAnswers})

    def ensureQuestionsAndAnswersIds(self, questions):
        """
        Ensure all questions and answers have ids.
        """
        # Create auto-id for each question if id absent
        resultedQuestions = [dict(self.ensureQuestionAnswersIds(
            q), **{'id': q['id'] if hasNotEmpty(q, 'id') else 'Q' + str(i + 1)}) for i, q in enumerate(questions)]
        # TODO: Remove `correct` field from answer items?
        return resultedQuestions

    def getQuestionsData(self, forceLoad=False):
        """
        Get questions data for server purposes (with `correct` fields).
        """
        data = self.getOrLoadQuestionsData(forceLoad=forceLoad)
        return data

    def getClientQuestionsData(self, forceLoad=False):
        """
        Get questions data for server purposes (without `correct` fields).
        """
        data = self.getOrLoadQuestionsData(forceLoad=forceLoad)
        data = dict(data, **{'questions': self.removeQuestionsCorrectAnswers(data['questions'])})
        return data

    def removeAnswerCorrectData(self, a):
        if 'correct' in a:
            newA = dict(a)
            newA.pop('correct', None)
            return newA
        return a

    def removeQuestionAnswersCorrectData(self, q):
        answers = q['answers']
        resultedAnswers = [self.removeAnswerCorrectData(a) for a in answers]
        #  resultedAnswers = map(self.removeAnswerCorrectData, answers)  # ???
        result = dict(q, **{'answers': resultedAnswers})
        #  DEBUG(getTrace('removeQuestionAnswersCorrectData'), {
        #      'q': q,
        #      'answers': answers,
        #      'resultedAnswers': resultedAnswers,
        #      'result': result,
        #  })
        return result

    def removeQuestionsCorrectAnswers(self, questions):
        """
        Remove `correct` field from answer items
        """
        # Remove `correct` fields
        resultedQuestions = [self.removeQuestionAnswersCorrectData(q) for q in questions]
        # resultedQuestions = map(self.removeQuestionAnswersCorrectData, questions)  # ???
        return resultedQuestions

    def getClientQuestionIdsList(self):
        """
        Prepare specified amount of questions for clients
        """
        data = self.getClientQuestionsData()
        qq = data['questions']
        qqCount = len(qq)
        count = qqCount
        if not count or count <= 0:
            return []
        ids = [a['id'] for a in qq]
        questionsCount = config['questionsCount']
        if questionsCount and questionsCount is not None and questionsCount < count:
            count = questionsCount
        useRandomQuestions = config['useRandomQuestions']
        if not useRandomQuestions:
            # Return first {count} questions if randomization isn't required
            return ids[0:count]
        list = []  # Result list
        while len(list) < count:
            if not len(ids):
                errStr = 'Questions list has unexpectedly flushed out!'
                DEBUG(getTrace('error'), {
                    'errStr': errStr,
                })
                raise Exception(errStr)
            rand = random()  # Random float:  0.0 <= x < 1.0
            qIdx = math.floor(rand * len(ids))
            id = ids[qIdx]
            if id not in list:
                list.append(id)
                ids.remove(id)
        #  DEBUG(getTrace('getClientQuestionIdsList'), {
        #      #  'qq': qq,
        #      'ids': ids,
        #      'questionsCount': questionsCount,
        #      'qqCount': qqCount,
        #      'count': count,
        #      'list': list,
        #  })
        return list


# Create singleton...
questions = Questions()


__all__ = [  # Exporting objects...
    'questions',
]


if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
