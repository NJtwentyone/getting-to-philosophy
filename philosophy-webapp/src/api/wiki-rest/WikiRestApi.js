class WikiRestApi {

static API = '/wiki/degreeOfSeperation/';

  /**
   returns path url
  */
  static urlPath(title) {
    return WikiRestApi.API + 'path/?title=' + title;
  }

  /**
   returns find url
  */
  static urlFind(title) {
    return WikiRestApi.API + 'find/?title=' + title;
  }

  /**
   returns status url
  */
  static urlStatus(title, sessionId) {
    let params = 'title=' + title;
    if (sessionId) { params += '&sessionId='+ sessionId; }
    return WikiRestApi.API + 'status/?' + params;
  }
}

export default WikiRestApi;
