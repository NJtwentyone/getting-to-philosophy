#from __future__ import absolute_import
from celery import shared_task
import logging
import os

# NOTE for local files, use '.' at beggining of path, for celery to find it
from .api.degree_of_seperation import DegreeOfSeperation, DegreeOfSeperationWiki, DegreeOfSeperationWikiThread
from .api.wiki_title import WikiTitle, WikiTitleRest
from .api.data_store import DataStore, DataStoreMongo, DataStoreMongoHybrid

logger = logging.getLogger(__name__)

def getDegreeOfSeperation():
    MONGO_SERVER_URL = os.environ.get('DJANGO_BENTO_MONGO_SERVER_URL', None)
    wikiTitle = WikiTitleRest()
    dataStore = DataStoreMongo(MONGO_SERVER_URL)
    degreeOfSeperation = DegreeOfSeperationWikiThread(dataStore, wikiTitle)
    return degreeOfSeperation

@shared_task  # Use this decorator to make this a asyncronous function
def asyncFindShortestPath(startTitle, endTitle, sessionId):
    logger.info("asyncFindShortestPath startTile: " + startTitle + " endTitle: " + endTitle + " sesssionId: " + sessionId)
    degreeOfSeperation = getDegreeOfSeperation()
    return degreeOfSeperation.findShortestPath(startTitle, endTitle, sessionId)