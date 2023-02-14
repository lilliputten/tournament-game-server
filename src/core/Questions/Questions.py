# -*- coding:utf-8 -*-
# @module Questions
# @desc Questions...
# @since 2023.02.15, 01:48
# @changed 2023.02.15, 02:26

from os import path
import yaml

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

#  from datetime import datetime
#  from tinydb import Query
#  # from tinydb.table import Document
#  from src import appSession
#  # from src.core.lib import serverUtils
#  from src.core.lib.Storage import Storage
#
#  from src.core.lib.logger import DEBUG, getDateStr, getMsTimeStamp
#  from src.core.lib.uniqueToken import createUniqueToken
#  from src.core.lib.utils import empty, getObjKey, getTrace, hasNotEmpty, notEmpty
#
#  from src.core.Waiting import WaitingHelpers, waitingStorage, WaitingConstants

from config import config


class Questions():

    testMode = None

    def __init__(self, testMode=False):
        self.testMode = testMode

    def getRootPath(self):
        rootPath = config['rootPath']
        # xx
        return rootPath

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
                return yaml.load(handler, Loader=yaml.FullLoader)
        return {}


# Create singleton...
questions = Questions()


__all__ = [  # Exporting objects...
    'questions',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
