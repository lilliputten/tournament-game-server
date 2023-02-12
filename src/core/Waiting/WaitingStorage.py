# -*- coding:utf-8 -*-
# @module WaitingStorage
# @desc Storage for waiting records
# @since 2023.02.12, 01:01
# @changed 2023.02.12, 01:42


#  import time
#  import sys
#  import json
import traceback
from os import path

import datetime

# TinyDB. @see: https://tinydb.readthedocs.io/en/latest/usage.html
from tinydb import TinyDB
from tinydb import Query
#  from tinydb import where
from tinydb.storages import JSONStorage
from tinydb.storages import MemoryStorage
from tinydb.middlewares import CachingMiddleware

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    #  getDateStr,
    getMsTimeStamp,
)
from src.core.lib.utils import getTrace

from src.core.Waiting import WaitingConstants
#  from src.core.Waiting import WaitingMail

dbName = WaitingConstants.dbName

dbFile = path.join(config['dbPath'], dbName + config['dbExt'])


class WaitingStorage():

    testMode = None

    hasDbChanges = False
    db = None  # Database handler

    def __init__(self, testMode=False):
        self.testMode = testMode

    def __del__(self):
        self.dbClose()

    def dbOpen(self):
        #  self.db = sqlite3.connect(dbFile)  # sqlite3
        #  self.db = TinyDB(dbFile)
        try:
            if self.testMode:
                # Use memory-based storage (basically during tests).
                db = TinyDB(storage=MemoryStorage)
            else:
                # Use real file-based storage.
                db = TinyDB(
                    dbFile,
                    storage=CachingMiddleware(JSONStorage),
                    sort_keys=True,
                    indent=2,
                    # Adding params to disable utf-8 quoting in json (`\uXXXX`)
                    encoding='UTF-8',
                    ensure_ascii=False,
                )
            self.db = db
            return db
        except Exception as err:
            #  sError = errors.toString(err, show_stacktrace=False)
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'err': err,
                'traceback': sTraceback,
            })
            raise err

    def getDbHandler(self):
        if self.db is not None and self.db._opened:
            return self.db
        return self.dbOpen()

    def dbClose(self):
        if self.db is not None:
            if self.db._opened:
                self.dbSave()
                self.db.close()
            self.db = None

    def dbSave(self):
        if self.db is not None:
            # TODO: Force write (flush) tinydb?
            if hasattr(self.db, 'storage') and hasattr(self.db.storage, 'flush'):
                # False-positive pyright error. TODO?
                self.db.storage.flush()  # type: ignore
            # self.db.commit()  # TODO: Check for hasDbChanges flag?
            self.hasDbChanges = False

    def dbSync(self):
        # Synchronyze memory data with disk data.
        if self.db is not None:
            self.db.clear_cache()

    def clearData(self):
        if self.db is not None:
            self.db.truncate()

    def getRecordsCount(self):
        db = self.getDbHandler()
        if db is not None:
            return len(db)
        return 0

    def getAllData(self):
        #  DEBUG(getTrace())
        try:
            db = self.getDbHandler()
            if db is not None:
                result = db.all()
                #  DEBUG(getTrace('result'), {
                #      'result': result,
                #  })
                return result
        except Exception as err:
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'err': err,
                'traceback': sTraceback,
            })
            #  #  errStr = 'Cannot execute db command: ' + dbCmd
            #  raise Exception(errStr) from err
            raise err
        return []

    def addRecord(self, timestamp=None, Token=None, data=None):
        """
        Add record with params:
        - timestamp (number)
        - Token (string)
        - data (dict)
        Returns created record id (from tinydb).
        """
        # Automatically set timestamp if absent?
        if timestamp is None or not timestamp:
            now = datetime.datetime.now()
            timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
        if not data or data is None:
            data = {}
        dbData = dict(data, **{
            'timestamp': timestamp,
            'Token': Token,
        })
        # DEBUG(getTrace(), {
        #     'dbData': dbData,
        #     'data': data,
        # })
        try:
            db = self.getDbHandler()
            if db is not None:
                recordId = db.insert(dbData)
                #  if not self.testMode:
                #      WaitingMail.sendRecordMail(dbData)
                return recordId
        except Exception as err:
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'dbData': dbData,
                'err': err,
                'traceback': sTraceback,
            })
            #  #  errStr = 'Cannot execute db command: ' + dbCmd
            #  raise Exception(errStr) from err
            raise err
        return None

    def findRecords(self, fragment):
        """
        `fragment`: data object with params:
        - `Token`: string,
        Returns found records list.
        """
        db = self.getDbHandler()
        if fragment and db is not None:
            try:
                # False-positive pyright error. TODO?
                return db.search(Query().fragment(fragment))  # type: ignore
            except Exception as err:
                sTraceback = str(traceback.format_exc())
                DEBUG(getTrace('catched error'), {
                    'err': err,
                    'traceback': sTraceback,
                })
                raise err
        return []

    def extractRecords(self, fragment):
        """
        Find and remove records using fragment (all parameters are optional):
        - `Token`: string,
        Returns found (and removed) records list.
        """
        records = self.findRecords(fragment)
        # Remove records
        if len(records):
            db = self.getDbHandler()
            if db is not None:
                ids = list(map(lambda rec: rec.doc_id, records))
                db.remove(doc_ids=ids)
        return records

    def removeRecords(self, fragment):
        """
        Remove records using fragment (all parameters are optional):
        - `Token`: string,
        """
        return self.extractRecords(fragment)


__all__ = [  # Exporting objects...
    'WaitingStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
