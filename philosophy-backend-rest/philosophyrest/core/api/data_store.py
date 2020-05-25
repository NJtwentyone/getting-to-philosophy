import abc
import requests
import json
from pymongo import MongoClient, DESCENDING
import datetime

class DataStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getTitlePaths(self, title):
        """TODO"""
        return

    @abc.abstractmethod
    def setTitlePaths(self, title, paths):
        """TODO"""
        return

    @abc.abstractmethod
    def getTitleLinks(self, title):
        """TODO"""
        return

    @abc.abstractmethod
    def setTitleLinks(self, title, links):
        """TODO"""
        return

    @abc.abstractmethod
    def hasVisitedTitle(self, sessionId, title):
        """TODO"""
        return

    @abc.abstractmethod
    def setVisitedTitle(self, sessionId, title, visited):
        """TODO"""
        return

    @abc.abstractmethod
    def getPreviousTitle(self, sessionId, title):
        """TODO"""
        return

    @abc.abstractmethod
    def setPreviousTitle(self, sessionId, title, previousTitle):
        """TODO"""
        return

    @abc.abstractmethod
    def cleanUp(self):
        """TODO"""
        return

    @abc.abstractmethod
    def getVisitedCount(self, sessionId):
        """TODO"""
        return

    @abc.abstractmethod
    def getSessionId(self, title):
        """TODO"""
        return

class DataStoreMongo(DataStore):
    def __init__(self, url = None):
        self._client = MongoClient(url if url else 'mongodb://localhost:27017')
        self._db = self._client['bento']
        self._tmpVisited = 'temp_visited_'
        self._tmpPrevious = 'temp_previous_'

    def getTitlePaths(self, titleName):
        try:
            dbTitle = self._db.title.find_one({'_id': titleName})
            return dbTitle['paths'] if dbTitle else None
        except KeyError as error:
            return None

    def setTitlePaths(self, titleName, paths, uid = ''):
        # TODO set uid or use generated uid or
        self._db.title.update({'_id': titleName}, {'$set': {'title': titleName, 'paths': paths }}, upsert = True)
        return

    def getTitleLinks(self, titleName):
        try:
            dbTitle = self._db.title.find_one({'_id': titleName})
            return dbTitle['links'] if dbTitle else None
        except KeyError as error:
            return None

    def setTitleLinks(self, titleName, links):
        self._db.title.update({'_id': titleName}, {'$set': {'title': titleName, 'links': links}}, upsert = True)
        return

    def _keyVisited(self, suffix):
        return self._tmpVisited + suffix

    def _keyPrevious(self, suffix):
        return self._tmpPrevious + suffix

    def hasVisitedTitle(self, sessionId, titleName):
        dynamicCollection = self._keyVisited(sessionId)
        dbVisited = self._db[dynamicCollection].find_one({'_id': titleName})
        return dbVisited['visited'] if dbVisited else False

    def setVisitedTitle(self, sessionId, titleName, visited):
        dynamicCollection = self._keyVisited(sessionId)
        self._db[dynamicCollection].update({'_id': titleName},{'$set': {'visited': visited}}, upsert = True)
        return

    def getPreviousTitle(self, sessionId, titleName):
        dynamicCollection = self._keyPrevious(sessionId)
        dbPrevious = self._db[dynamicCollection].find_one({'_id': titleName})
        return dbPrevious['previous'] if dbPrevious else False

    def setPreviousTitle(self, sessionId, titleName, previousTitle):
        dynamicCollection = self._keyPrevious(sessionId)
        self._db[dynamicCollection].update({'_id': titleName}, {'$set': {'previous': previousTitle}}, upsert = True)
        return

    def setUp(self, sessionId, titleName):
        self._db.metric.update({'_id': sessionId},{'$set': {'timeStart': datetime.datetime.now(), 'title': titleName}}, upsert = True)

    def cleanUp(self, sessionId):
        result_count = self.getVisitedCount(sessionId)
        self._db.metric.update({'_id': sessionId},{'$set': {'timeEnd': datetime.datetime.now(), 'visitedCount': result_count}}, upsert = True)

        collections = self._db.collection_names(include_system_collections=False)
        for collection in collections:
            if self._tmpVisited in collection or self._tmpPrevious in collection:
                self._db[collection].drop()
        return

    def getVisitedCount(self, sessionId):
        key = self._keyVisited(sessionId)
        results = self._db[key].find()
        return results.count()

    def getSessionId(self, title):
        results = self._db.metric.find({'title': title}, {'_id': 1}).sort('timeStart', DESCENDING).limit(1)
        return results[0]['_id'] if results.count() > 0 else None

class DataStoreMongoHybrid(DataStoreMongo):
    def __init__(self, url = 'mongodb://localhost:27017'):
        super(DataStoreMongoHybrid, self).__init__(url)
        self._visited = {}
        self._previous = {}

    def hasVisitedTitle(self, sessionId, titleName):
        try:
            return self._visited[titleName]
        except KeyError as error:
            return False

    def setVisitedTitle(self, sessionId, titleName, visited):
        self._visited[titleName] = visited
        return

    def getPreviousTitle(self, sessionId, titleName):
        try:
            return self._previous[titleName]
        except KeyError as error:
            return False

    def setPreviousTitle(self, sessionId, titleName, previousTitle):
        self._previous[titleName] = previousTitle
        return

    def getVisitedCount(self, sessionId):
        return len(self._visited)

    def getSessionId(self, title):
        # TODO find sessionId or best guess
        return None
