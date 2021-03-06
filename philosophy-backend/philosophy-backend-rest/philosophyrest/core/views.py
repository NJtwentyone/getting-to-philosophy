# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import logging
import json
import os
from api.degree_of_seperation import DegreeOfSeperation, DegreeOfSeperationWiki, DegreeOfSeperationWikiThread
from api.wiki_title import WikiTitle, WikiTitleRest
from api.data_store import DataStore, DataStoreMongo, DataStoreMongoHybrid
from api.create_response import createResponsePath, createResponseFind, createResponseStatus
from api.utils import randomStr
import tasks
import pdb

logger = logging.getLogger(__name__)

def getDegreeOfSeperation():
    MONGO_SERVER_URL = os.environ.get('DJANGO_BENTO_MONGO_SERVER_URL', None)
    wikiTitle = WikiTitleRest()
    dataStore = DataStoreMongo(MONGO_SERVER_URL)
    degreeOfSeperation = DegreeOfSeperationWikiThread(dataStore, wikiTitle)
    #degreeOfSeperation = DegreeOfSeperationWiki(dataStore, wikiTitle)
    return degreeOfSeperation

def getShortestPath(title):
    degreeOfSeperation = getDegreeOfSeperation()
    return degreeOfSeperation.getShortestPath(title, "Philosophy")

def findShortestPath(title, sessionId):
    degreeOfSeperation = getDegreeOfSeperation()
    return degreeOfSeperation.findShortestPath(title, "Philosophy", sessionId)

def statusShortestPath(title, sessionId):
    degreeOfSeperation = getDegreeOfSeperation()
    return degreeOfSeperation.statusShortestPath(sessionId, title, "Philosophy")

def DegreeOfSeperationPath(request):
    title = request.GET.get('title', '')
    logger.info("operation PATH for 'title' : " + title)
    try:
        shortestPath = getShortestPath(title)
        pathsResponseMap = createResponsePath(title, shortestPath)
        return JsonResponse(pathsResponseMap)
    except ValueError as e:
        logger.error("Exception caught:" + e)
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def DegreeOfSeperationFind(request):
    title = request.GET.get('title', '')
    sessionId = randomStr()
    logger.info("operation FIND for 'title' : " + title + ", 'sessionId' : " + sessionId)
    try:
        ## async
        #tasks.asyncFindShortestPath.delay(title, "Philosophy", sessionId)
        ## FIXME copy of DegreeOfSeperationStatus
        #xstatusShortestPath = statusShortestPath(title, sessionId)
        #statusResponseMap = createResponseStatus(title, xstatusShortestPath)
        #return JsonResponse(statusResponseMap)

        # sync code for debugging
        #pdb.set_trace()
        findshortestPath = findShortestPath(title, sessionId)
        findResponseMap = createResponseFind(title, findshortestPath)
        return JsonResponse(findResponseMap)
        # TODO guard against repeat requests
    except ValueError as e:
        logger.error("Exception caught:" + e)
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def DegreeOfSeperationStatus(request):
    title = request.GET.get('title', '')
    sessionId = request.GET.get('sessionId', None)
    logger.info("operation STATUS for 'title' : " + title + " 'sessionId' : " + sessionId)
    try:
        xstatusShortestPath = statusShortestPath(title, sessionId)
        statusResponseMap = createResponseStatus(title, xstatusShortestPath)
        return JsonResponse(statusResponseMap)
    except ValueError as e:
        logger.error("Exception caught:" + e)
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
