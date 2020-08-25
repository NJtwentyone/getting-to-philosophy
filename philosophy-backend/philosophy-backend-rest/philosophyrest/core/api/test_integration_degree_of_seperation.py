import unittest
import sys
from pstats import Stats
import logging
from mock import Mock
from degree_of_seperation import DegreeOfSeperationWiki
from ..lib.data_struct import PeekQueue
from wiki_title import WikiTitle
from data_store import DataStore, DataStoreMongo

logger = logging.getLogger()
logger.level = logging.DEBUG

class WikiTitleTestStub(WikiTitle):
    def __init__(self, linksMap):
        self.linksMap = linksMap

    def getTitleLinks(self, title):
        return self.linksMap[title]

class TestDegreeOfSeperationInt(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)


    def test_findShortestPath(self):
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

        dataStoreMongo = DataStoreMongo()
        #wtf = dataStoreMongo.getTitlePaths("t")
        #logging.getLogger().info("wtf:" + wtf)
        stubWikiApi = WikiTitleTestStub(restLinksMap)
        dos = DegreeOfSeperationWiki(dataStoreMongo, stubWikiApi)
        result = dos.findShortestPath(nodeA, nodeD)
        self.assertEqual(result, expectedPath)

if __name__ == '__main__':
    unittest.main()
