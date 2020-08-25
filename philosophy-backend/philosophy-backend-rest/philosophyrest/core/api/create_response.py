import json

def createResponsePath(startTitle, paths):
    jsonMap = {'searchTitle' : startTitle}
    if paths is None:
        jsonMap['errors'] = "error_code_01_tdne - title doesn't exist"
        return jsonMap

    if paths is False:
        jsonMap['status'] = 'no_data'
    else:
        jsonMap['status'] = 'data'
        jsonMap['pathTitles'] = paths

    return jsonMap

def createResponseFind(startTitle, paths):

    return createResponsePath(startTitle, paths)

def createResponseStatus(startTitle, statusMap):
    jsonMap = statusMap.copy()
    jsonMap['searchTitle'] = startTitle

    if len(statusMap) == 0:
        jsonMap['status'] = 'NO_DATA'
        return jsonMap

    percentComplete = int(statusMap['x'])/int(statusMap['y'])
    jsonMap['status'] = 'COMPLETE' if percentComplete == 1 else 'NOT_COMPLETE'

    return jsonMap
