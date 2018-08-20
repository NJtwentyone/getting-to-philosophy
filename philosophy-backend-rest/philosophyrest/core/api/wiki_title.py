import abc
import requests
import json

class WikiTitle(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getTitleLinks(self, title):
        """Retrieve assoicated wiki title 'links' to this title"""
        return

class WikiTitleRest(WikiTitle):
    def __init__(self):
        self._baseUrl = 'https://en.wikipedia.org/' \
            + 'w/api.php?action=parse&format=json&prop=links&page='

    def getTitleLinks(self, title):
        responseJson = self._makeRestCall(title)
        if 'error' in responseJson:
            return False
            
        return self._extractTitlesJson(responseJson)

    def _makeRestCall(self, title):
        # TODO clean title ie convert space to '_'
        response = requests.post(self._baseUrl + title)
        #check response coded ie response.status_code
        return response.json()

    def _extractTitlesJson(self, jsonWikiResponse):
        titles = []
        try:
            for link in jsonWikiResponse['parse']['links']:
                titles.append(link['*'])
            return titles
        except KeyError as error:
            return []
