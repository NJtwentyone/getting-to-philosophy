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
import logging

logger = logging.getLogger(__name__)

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
        logger.debug("startTitle: '%s', paths: %d,  neighbors: %s ..." % (startTitle, paths) )
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

    def _getNeighborTitlesHelper(self, title, cacheResults=True):
        dbTitleNeighbors = self._dataStore.getTitleLinks(title)
        if dbTitleNeighbors:
            return dbTitleNeighbors

        restTitleNeighbors = self._restApi.getTitleLinks(title)
        if restTitleNeighbors is False:
            restTitleNeighbors = []

        if cacheResults is True:
            self._dataStore.setTitleLinks(title, restTitleNeighbors)

        logger.debug("title: '%s', len(neighbors): %d,  neighbors: %s ..." % (title, len(restTitleNeighbors), str(restTitleNeighbors)[:300] ) )
        return restTitleNeighbors

class DegreeOfSeperationWikiThread(DegreeOfSeperationWiki):
    def __init__(self, dataStore, restApi, threadCount = 100, timeout=2):
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
        for worker_id in range(1):
            thread_args = [self, worker_id, 0, numWorkers, endTitle, sessionId, getTimeout, pQueue, msgQueue, retQueue]
            threads.append(Thread(target=determinePathsHelperWorker, args=thread_args))
            threads[-1].start()

        for thread in threads:
           thread.join()

        return self._constructPath(sessionId, None if retQueue.empty() else endTitle)

def determinePathsHelperWorker(degreeOfSeperation, worker_id, assigned_distance, num_workers, end_title, session_id, get_timeout, p_queue, msg_queue, ret_queue):

    processing_distance = -1
    while True:
        if recievedStopMessage(worker_id, msg_queue):
            return

        item = None

        try:
            item = p_queue.get(block=True, timeout=get_timeout)
        except Empty:
            if worker_id == 0:
                # master, assume if can't find work, then empty
                for _ in range(num_workers - 1):
                    logger.debug("id: '%d' (master) [queue] is empty" % (worker_id))
                    msg_queue.put(('NOT_FOUND', {'time': datetime.datetime.now()}))
                break
                # else worker thread do nothing continue

        if item == None:
            continue

        current_distance, current_title = item

        # goal slow start at beginning so threads to processing multiple distances
        # master node AND changed to new current_distance AND queue has enough work for other nodes
        if worker_id == 0 and processing_distance != current_distance and current_distance >= 1:
            processing_distance = current_distance
            total_num_workers = num_workers if p_queue.qsize() > 2 * num_workers else min(p_queue.qsize()/2, num_workers)

            for new_worker_id in range(1, total_num_workers):
                thread_args = [degreeOfSeperation, new_worker_id, current_distance, num_workers, end_title, session_id, get_timeout, p_queue, msg_queue, ret_queue]
                thread = Thread(target=determinePathsHelperWorker, args=thread_args)
                thread.start()

        """
        goal only spawn worker threads for specific distance
        once done with level terminate
        don't want to do coordination messages, and there isn't a queue.peek()
        so dequeue item, if not level, put back and then terminate
        """
        if worker_id != 0 and current_distance != assigned_distance:
            p_queue.put(item)
            return

        logger.debug("id: '%d' [dequeue] current_distance: %d current_title: '%s'  len(pQueue): %d" % (worker_id, current_distance, current_title, p_queue.qsize()))

        for idx, neighborTitle in enumerate(degreeOfSeperation._getNeighborTitles(current_title, randomSort=True)):

            if idx % 100 == 0:
                logger.debug("id: '%d' [add] neighbor_distance: %d neighborTitle: '%s' neighbor_title#: %d " % (worker_id, current_distance + 1, neighborTitle, idx,))
                # stop processing neighbor early
                if recievedStopMessage(worker_id, msg_queue):
                    logger.debug("id: '%d' [stop] processing neighbors" % (worker_id))
                    return

            if not degreeOfSeperation._hasVisited(session_id, neighborTitle):
                # '(current_distance + 1...' preserve BFS shortest current_distance processing between threads
                p_queue.put((current_distance + 1, neighborTitle))
                degreeOfSeperation._setVisited(session_id, neighborTitle, True)
                degreeOfSeperation._setPreviousTitle(session_id, neighborTitle, current_title)

            if neighborTitle == end_title:
                for _ in range(num_workers):
                    msg_queue.put(('FOUND', {'time': datetime.datetime.now()}))
                logger.debug("id: '%d' [found] '%s' issuing FOUND msg to all threads" % (worker_id, end_title))
                ret_queue.put({'title' : end_title, 'time': datetime.datetime.now()})
                break

def recievedStopMessage(id, msgQueue):
    try:
        msq = msgQueue.get(block=False)
        if msq[0] == 'FOUND' or msq[0] == 'NOT_FOUND':
            logger.debug("id: '%d' ordered to stop by msg : %s len(msqQueue): %d" % (id, msq[0], msgQueue.qsize()) )
            return True
    except Empty:
        return False
