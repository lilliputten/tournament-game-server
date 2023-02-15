# -*- coding:utf-8 -*-
# @module Questions
# @desc Questions...
# @since 2023.02.15, 01:48
# @changed 2023.02.16, 00:51

from os import path
import yaml

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace, hasNotEmpty

from config import config


class Questions():

    testMode = None
    questions = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def getFileName(self):
        rootPath = config['rootPath']
        file = path.join(rootPath, 'questions.yaml')
        if path.isfile(file):
            return file
        file = path.join(rootPath, 'questions.default.yaml')
        if path.isfile(file):
            return file
        return None

    def loadQuestions(self):
        file = self.getFileName()
        if file and path.isfile(file):
            with open(file, encoding='UTF-8') as handler:
                self.questions = yaml.load(handler, Loader=yaml.FullLoader)
                return self.questions
        return {}

    def getQuestions(self, forceLoad=False):
        # TODO: Do forceLoad time-dependent
        questions = self.questions
        if questions is None or forceLoad:
            questions = self.loadQuestions()
        return questions

    def getClientQuestionsData(self, forceLoad=False):
        srcData = self.getQuestions(forceLoad=forceLoad)
        questions = srcData['questions']
        # Create auto-id for each question if id absent
        resultedQuestions = [dict(q, **{'id': q['id'] if hasNotEmpty(q, 'id') else 'Q' + str(i + 1)}) for i, q in enumerate(questions)]
        # TODO: Remove `correct` field from answer items?
        return {'questions': resultedQuestions}


# Create singleton...
questions = Questions()


__all__ = [  # Exporting objects...
    'questions',
]


if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
