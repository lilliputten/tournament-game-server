# -*- coding:utf-8 -*-
# @module Storage
# @desc Storage for waiting records
# @since 2023.02.12, 20:38
# @changed 2023.02.12, 20:38


import traceback
from os import path

import datetime

# TinyDB. @see: https://tinydb.readthedocs.io/en/latest/usage.html
from tinydb import TinyDB
from tinydb import Query
from tinydb.storages import JSONStorage
from tinydb.storages import MemoryStorage
from tinydb.middlewares import CachingMiddleware

from config import config
from src.core.lib.errors import toString

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getMsTimeStamp,
)
from src.core.lib import tinydbUtils
from src.core.lib.utils import getTrace


class Storage():

    testMode = None

    db = None  # Database handler
    dbName = None

    def __init__(self, testMode=False, dbName=None):
        self.testMode = testMode
        self.dbName = dbName

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
                if not self.dbName:
                    raise Exception('dbName isnt defined!')
                dbFile = path.join(config['dbPath'], self.dbName + config['dbExt'])
                # Use real file-based storage.
                db = TinyDB(
                    dbFile,
                    storage=CachingMiddleware(JSONStorage),
                    sort_keys=True,
                    indent=2,
                    # Adding params to disable utf-8 quoting in json (`\uXXXX`)
                    encoding='UTF-8',
                    ensure_ascii=False,
                    # TODO: To set parameter for using unix EOLs?
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
        if self.db is not None and tinydbUtils.isDbOpened(self.db):
            return self.db
        return self.dbOpen()

    def dbClose(self):
        if self.db is not None:
            if tinydbUtils.isDbOpened(self.db):
                self.dbSave()
                self.db.close()
            self.db = None

    def dbSave(self):
        if self.db is not None:
            # TODO: Force write (flush) tinydb?
            if hasattr(self.db, 'storage') and hasattr(self.db.storage, 'flush'):
                # False-positive pyright error. TODO?
                self.db.storage.flush()  # type: ignore

    def isOpened(self):
        # Synchronyze memory data with disk data.
        if self.db is not None and tinydbUtils.isDbOpened(self.db):
            return True
        return False

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
        try:
            db = self.getDbHandler()
            if db is not None:
                result = db.all()
                return result
        except Exception as err:
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'err': err,
                'traceback': sTraceback,
            })
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
        # Check Token...
        if Token is None or not Token:
            if data and data is not None and 'Token' in data and data['Token'] is not None:
                Token = data['Token']
        # Automatically set timestamp if absent?
        if timestamp is None or not timestamp:
            if data and data is not None and 'timestamp' in data and data['timestamp'] is not None:
                timestamp = data['timestamp']
            else:
                timestamp = getMsTimeStamp(datetime.datetime.now())  # Get milliseconds timestamp (for technical usage)
        if not data or data is None:
            data = {}
        dbData = dict(data, **{
            'timestamp': timestamp,
            'Token': Token,
        })
        try:
            db = self.getDbHandler()
            if db is not None:
                recordId = db.insert(dbData)
                return recordId
        except Exception as err:
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'dbData': dbData,
                'err': err,
                'traceback': sTraceback,
            })
            raise err
        return None

    def findRecords(self, query):
        """
        `query`: query or fragment (data object with params):
        - `Token`: string,
        Returns found records list.
        """
        db = self.getDbHandler()
        if query and db is not None:
            try:
                # Convert to query if fragment passed...
                if not tinydbUtils.isQuery(query):
                    query = Query().fragment(query)
                # False-positive pyright error. TODO?
                return db.search(query)  # type: ignore
            except Exception as err:
                errStr = 'Error reading internal storage `' + str(self.dbName) + '`: ' + toString(err)
                sTraceback = str(traceback.format_exc())
                DEBUG(getTrace('catched error'), {
                    'errStr': errStr,
                    'err': err,
                    'traceback': sTraceback,
                })
                #  raise err
                raise Exception(errStr)
        return []

    def findFirstRecord(self, query):
        """
        `query`: query or fragment (data object with params):
        - `Token`: string,
        Get first found record.
        """
        records = self.findRecords(query)
        if len(records):
            return records[0]
        return None

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
    'Storage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
