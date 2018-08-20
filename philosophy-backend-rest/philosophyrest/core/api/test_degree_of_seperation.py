import unittest
from mock import Mock
from degree_of_seperation import DegreeOfSeperationWiki
from data_struct import PeekQueue
from wiki_title import WikiTitle
from data_store import DataStore

class DataStoreTestStub(DataStore):
    def __init__(self):
        self.pathsMap = {}
        self.linksMap = {}
        self.visitedMap = {}
        self.previousMap = {}

    def getTitlePaths(self, title):
        try:
            return self.pathsMap[title]
        except KeyError as error:
            return False

    def setTitlePaths(self, title, paths):
        self.pathsMap[title] = paths
        return

    def getTitleLinks(self, title):
        try:
            return self.linksMap[title]
        except KeyError as error:
            return False

    def setTitleLinks(self, title, links):
        self.linksMap[title] = links
        return

    def hasVisitedTitle(self, sessionId, title):
        try:
            return self.visitedMap[title]
        except KeyError as error:
                return False

    def setVisitedTitle(self, sessionId, title, visited):
        self.visitedMap[title] = visited
        return

    def getPreviousTitle(self, sessionId, title):
        return self.previousMap[title]

    def setPreviousTitle(self, sessionId, title, previousTitle):
        self.previousMap[title] = previousTitle
        return

    def cleanUp(self):
        return

    def getVisitedCount(self, sessionId):
        return -1

    def getSessionId(self, title):
        return -1

class WikiTitleTestStub(WikiTitle):
    def __init__(self, linksMap):
        self.linksMap = linksMap

    def getTitleLinks(self, title):
        return self.linksMap[title]

class TestDegreeOfSeperationWiki(unittest.TestCase):

    def test__randomStr(self):
        dos = DegreeOfSeperationWiki(None, None)
        ids = set()
        testSize = 1000

        for _ in xrange(testSize):
            ids.add(dos._randomStr())

        # just need them to unique
        self.assertEqual(len(ids), testSize)

    def test__getNeighborTitles_datastore(self):
        mock_datatStore = Mock(name='dataStore')
        expectedLinks = ['A', 'B', 'C']
        mock_datatStore.getTitleLinks.return_value = expectedLinks
        dos = DegreeOfSeperationWiki(mock_datatStore, None)
        result = dos._getNeighborTitles("Alphabet")
        self.assertEqual(expectedLinks, result)

    def test__getNeighborTitles_restWiki(self):
        mock_datatStore = Mock(name='dataStore')
        mock_restWiki = Mock(name='restWiki')
        expectedLinks = ['1', '2', '3']
        mock_datatStore.getTitleLinks.return_value = False
        mock_restWiki.getTitleLinks.return_value = expectedLinks
        dos = DegreeOfSeperationWiki(mock_datatStore, mock_restWiki)
        result = dos._getNeighborTitles("Alphabet")
        self.assertEqual(expectedLinks, result)
        mock_datatStore.setTitleLinks.assert_called_with("Alphabet", expectedLinks)

    def test__getNeighborTitles_restWiki_Error(self):
        mock_datatStore = Mock(name='dataStore')
        mock_restWiki = Mock(name='restWiki')
        expectedLinks = []
        mock_datatStore.getTitleLinks.return_value = False
        mock_restWiki.getTitleLinks.return_value = expectedLinks
        dos = DegreeOfSeperationWiki(mock_datatStore, mock_restWiki)
        result = dos._getNeighborTitles("File:Map.jpg")
        self.assertEqual(expectedLinks, result)
        mock_datatStore.setTitleLinks.assert_called_with("File:Map.jpg", expectedLinks)

    def test__constructPath(self):
        mock_datatStore = Mock(name='dataStore')
        expectedPath = ['Alpha', 'Beta', 'Gamma']
        sessionId = 'testId'
        # TODO tie mock return to arguments
        #mock_datatStore.side_effect = {(sessionId,'Gamma'): 'Beta', (sessionId,'Beta'): 'Alpha', (sessionId,'Alpha'): None }
        mock_datatStore.getPreviousTitle.side_effect = ['Beta', 'Alpha', None ]
        dos = DegreeOfSeperationWiki(mock_datatStore, None)
        result = dos._constructPath(sessionId, 'Gamma')
        self.assertEqual(result, expectedPath)

    """
    Testing simple graph case:
        A --> B
        |    /|
        |  /  |
        v v   v
        C <-- D
    """
    def test__determinePathsHelper(self):
        nodeA = 'A'
        nodeB = 'B'
        nodeC = 'C'
        nodeD = 'D'
        restLinksMap = {}
        restLinksMap[nodeA] = [nodeB, nodeC]
        restLinksMap[nodeB] = [nodeD]
        restLinksMap[nodeC] = []
        restLinksMap[nodeD] = [nodeC]
        expectedPath = [nodeA, nodeB, nodeD]

        stubDataStore = DataStoreTestStub()
        stubWikiApi = WikiTitleTestStub(restLinksMap)
        dos = DegreeOfSeperationWiki(stubDataStore, stubWikiApi)
        queue = PeekQueue()
        result = dos._determinePathsHelper(nodeA, nodeD, 'sessionId', queue)
        self.assertEqual(result, expectedPath)
