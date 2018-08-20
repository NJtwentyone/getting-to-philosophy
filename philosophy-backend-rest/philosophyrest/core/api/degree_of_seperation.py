import sys
import abc
import datetime
import random
from threading import Lock, Thread
from data_struct import PeekQueue
from Queue import Queue, PriorityQueue, Empty
from wiki_title import WikiTitle
from data_store import DataStore
from utils import randomStr



class DegreeOfSeperation(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getShortestPath(self, startName, endName):
        """Retrieve shortest path for start to end ie [startName,..., endName]"""
        return

    @abc.abstractmethod
    def findShortestPath(self, startName, endName, sessionId = None):
        """Determine shortest path from start to end ie [startName,..., endName]."""
        return

    @abc.abstractmethod
    def statusShortestPath(self, sessonId, startName = None, endName = None):
        """Report status for sortestpath for start to finish ie [startName,..., endName]"""
        return

class DegreeOfSeperationWiki(DegreeOfSeperation):

    def __init__(self, dataStore, restApi):
        self._dataStore = dataStore
        self._restApi = restApi

    #
    # returns:
    #   [startName, ... endName] - if shortest path exists
    #   [] - if not path exists
    #   False - if valid title, but shortest path hasn't been determined
    #   None - if invalid title
    def getShortestPath(self, startName, endName):
        # TODO handle if invalid startTitle, -1 in paths or put 'errors' field
        # TODO clean all data replace " " with "_"
        paths = self._retrievePaths(startName)

        if paths:
            return paths

        return False if self._restApi.getTitleLinks(startName) else None

    def findShortestPath(self, startName, endName, sessionId = None):
        id = sessionId if sessionId else self._randomStr()
        newPaths = self._findShortestPathHelper(startName, endName, id)
        return {'paths' : newPaths, 'sessionId' : id}

    def _findShortestPathHelper(self, startName, endName, sessionId):
        newPaths = self._determinePaths(startName, endName, sessionId)

        if len(newPaths) > 0:
            self._createPathsForChildren(newPaths)

        return newPaths

    def statusShortestPath(self, sessonId, startName = None, endName = None):

        paths = self._retrievePaths(startName)

        if paths:
            return {'type' : 'x/y', 'x' : '1', 'y': '1'}

        # if not completed check internal state
        statusSessionId = sessonId if sessonId else self._dataStore.getSessionId(startName)
        if statusSessionId == None:
            return {}

        visitedCount = self._dataStore.getVisitedCount(statusSessionId)

        # estimated ~5M english wiki pages
        return {'type': 'x/y' , 'x': visitedCount , 'y' : '5000000', 'sessionId' : sessonId}

    def _retrievePaths(self, title):
        # if no result -> False
        return self._dataStore.getTitlePaths(title)

    def _createResponseJson(self, startTitle, paths):
        return createResponse(startTitle, paths)

    def _createPathsForChildren(self, newPaths):
        # since DFS gurantees the shortest path from 1... N, where N is the start title
        # by induction the N-1...1 is one of the shortest path for title N-1, where N-1, is
        # on less hop

        for idx in range(len(newPaths)):
            self._dataStore.setTitlePaths(newPaths[idx], newPaths[idx:])

    def _determinePaths(self, startTitle, endTitle, sessionId):
        queue = PeekQueue()
        self._setUp(sessionId, startTitle)
        paths = self._determinePathsHelper(startTitle, endTitle, sessionId, queue)
        self._cleanUp(sessionId)
        return paths

    def _determinePathsHelper(self, startTitle, endTitle, sessionId, queue):

        queue.add(startTitle)
        self._setVisited(sessionId, startTitle, True)
        self._setPreviousTitle(sessionId, startTitle, None)
        found = False

        while not queue.isEmpty() and not queue.peek() == endTitle and  not found:
            currentTitle = queue.remove()

            for neighborTitle in self._getNeighborTitles(currentTitle, randomSort=True):
                if not self._hasVisited(sessionId, neighborTitle):
                    queue.add(neighborTitle)
                    self._setVisited(sessionId, neighborTitle, True)
                    self._setPreviousTitle(sessionId, neighborTitle, currentTitle)

                if neighborTitle == endTitle:
                    found = True
                    break

        return self._constructPath(sessionId, None if queue.isEmpty() else endTitle)

    def _constructPath(self, sessionId, endNodeTitle):
        paths = []
        currentTitle = endNodeTitle

        while(currentTitle):
            paths.append(currentTitle)
            currentTitle = self._getPreviousTitle(sessionId, currentTitle)

        return paths[::-1]

    def _setVisited(self, sessionId, title, visited):
        self._dataStore.setVisitedTitle(sessionId, title, visited)

    def _hasVisited(self, sessionId, title):
        return self._dataStore.hasVisitedTitle(sessionId, title)

    def _getPreviousTitle(self, sessionId, title):
        return self._dataStore.getPreviousTitle(sessionId, title)

    def _setPreviousTitle(self, sessionId, title, previousTitle):
        self._dataStore.setPreviousTitle(sessionId, title, previousTitle)

    def _cleanUp(self, sessionId):
        self._dataStore.cleanUp(sessionId)

    def _setUp(self, sessionId, titleName):
        self._dataStore.setUp(sessionId, titleName)

    def _randomStr(self, size=8):
        return randomStr(size)

    def _getNeighborTitles(self, title, randomSort = False):
        restTitleNeighbors = self._getNeighborTitlesHelper(title)
        if randomSort:
            random.shuffle(restTitleNeighbors)
        # TODO return list of tuples (title, hasShortestPath) to short-circuit bfs
        # or (title, [atitle...endTitle])
        return restTitleNeighbors

    def _getNeighborTitlesHelper(self, title):
        dbTitleNeighbors = self._dataStore.getTitleLinks(title)
        if dbTitleNeighbors:
            return dbTitleNeighbors

        restTitleNeighbors = self._restApi.getTitleLinks(title)
        if restTitleNeighbors is False:
            restTitleNeighbors = []
        self._dataStore.setTitleLinks(title, restTitleNeighbors)

        return restTitleNeighbors

class DegreeOfSeperationWikiThread(DegreeOfSeperationWiki):
    def __init__(self, dataStore, restApi, threadCount = 5, timeout=10):
        super(DegreeOfSeperationWikiThread, self).__init__(dataStore, restApi)
        self._threadCount = threadCount
        self._getTimeout = timeout


    def _determinePathsHelper(self, startTitle, endTitle, sessionId, queue):

        numWorkers = self._threadCount
        getTimeout = self._getTimeout
        msgQueue = Queue()
        retQueue = Queue()
        pQueue = PriorityQueue()
        # for priority queue, priority = BFS level
        pQueue.put((0, startTitle))
        self._setVisited(sessionId, startTitle, True)
        self._setPreviousTitle(sessionId, startTitle, None)

        # break off into thread function
        threads = []
        for id in range(numWorkers):
            threads.append(Thread(target=determinePathsHelperWorker, args=(self, id, numWorkers, endTitle, sessionId, getTimeout, pQueue, msgQueue, retQueue)))
            threads[-1].start()

        for thread in threads:
           thread.join()

        return self._constructPath(sessionId, None if retQueue.empty() else endTitle)

def determinePathsHelperWorker(degreeOfSeperation, id, numWorkers, endTitle, sessionId, getTimeout, pQueue, msgQueue, retQueue):

    while True:
        try:
            msq = msgQueue.get(block=False)
            if msq[0] == 'FOUND' or msq[0] == 'NOT_FOUND':
                break
        except Empty:
            pass
            # do nothing continue

        item = None

        try:
            item = pQueue.get(block=True, timeout=getTimeout)
        except Empty:
            if id == 0:
                # master, assume if can't find work, then empty
                for _ in range(numWorkers - 1):
                    msgQueue.put(('NOT_FOUND', {'time': datetime.datetime.now()}))
                break
                # else worker thread do nothing continue

        if item == None:
            continue

        distance, currentTitle = item

        for neighborTitle in degreeOfSeperation._getNeighborTitles(currentTitle, randomSort=True):
            if not degreeOfSeperation._hasVisited(sessionId, neighborTitle):
                # '(distance + 1...' preserve BFS shortest distance processing between threads
                pQueue.put((distance + 1, neighborTitle))
                degreeOfSeperation._setVisited(sessionId, neighborTitle, True)
                degreeOfSeperation._setPreviousTitle(sessionId, neighborTitle, currentTitle)

            if neighborTitle == endTitle:
                for _ in range(numWorkers):
                    msgQueue.put(('FOUND', {'time': datetime.datetime.now()}))
                retQueue.put({'title' : endTitle, 'time': datetime.datetime.now()})
                break
