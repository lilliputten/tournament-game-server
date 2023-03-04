# -*- coding:utf-8 -*-
# @module Questions_test
# @since 2023.02.15, 01:53
# @changed 2023.03.04, 18:40

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k Questions`
#  - `python -m unittest -f src/core/Records/Questions_test.py`

import unittest

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from .Questions import Questions


print('\nRunning tests for', getTrace())


questions = Questions(testMode=True)


class Test_Questions(unittest.TestCase):

    #  def setUp(self):  # TODO: Initializations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        pass

    def test_getFileName(self):
        """
        getFileName
        """
        print('\nRunning test', getTrace())
        fileName = questions.getFileName()
        self.assertTrue(fileName)

    def test_loadQuestions(self):
        """
        loadQuestionsData
        """
        print('\nRunning test', getTrace())
        data = questions.loadQuestionsData()
        self.assertTrue(data)

    def test_getClientQuestionsData(self):
        """
        getClientQuestionsData
        """
        print('\nRunning test', getTrace())
        data = questions.getClientQuestionsData()
        self.assertTrue(data)

    def test_removeQuestionsCorrectAnswers(self):
        """
        removeQuestionsCorrectAnswers
        """
        print('\nRunning test', getTrace())
        qq = [{'question': 'Question text', 'answers': [{'text': 'Answer text', 'correct': True}]}]
        data = questions.removeQuestionsCorrectAnswers(qq)
        self.assertTrue(data)

    def test_removeQuestionAnswersCorrectData(self):
        """
        removeQuestionAnswersCorrectData
        """
        print('\nRunning test', getTrace())
        q = {'question': 'Question text', 'answers': [{'text': 'Answer text', 'correct': True}]}
        newQ = questions.removeQuestionAnswersCorrectData(q)
        self.assertTrue('correct' not in newQ['answers'][0])

    def test_removeAnswerCorrectData(self):
        """
        removeAnswerCorrectData
        """
        print('\nRunning test', getTrace())
        a = {'text': 'Answer text', 'correct': True}
        newA = questions.removeAnswerCorrectData(a)
        self.assertTrue('correct' in a)
        self.assertTrue('correct' not in newA)

    def test_getClientQuestionIdsList(self):
        """
        getClientQuestionIdsList
        """
        print('\nRunning test', getTrace())
        qq = questions.getClientQuestionsData()['questions']
        qqCount = len(qq)
        questionsCount = config['questionsCount']
        count = min(qqCount, questionsCount)
        data = questions.getClientQuestionIdsList()
        self.assertTrue(len(data) == count)


if __name__ == '__main__':
    DEBUG(getTrace(' test run'))
    unittest.main()
