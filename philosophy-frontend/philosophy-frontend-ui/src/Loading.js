import React, { Component } from 'react';
import axios from 'axios';
import WikiRestApi from './api/wiki-rest/WikiRestApi'
import loading from './hourglass.jpg';

class Loading extends Component {
  constructor(props) {
    super(props);
    this.state = {messages: []};
  }

  componentDidMount() {
    this.tick(); // show loading immediately
    this.timerID = setInterval(
      () => this.tick(),
      // every 1minute
      60000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  async tick() {

    if (!this.props.isLoading) { return; } // FIXME this guard shouldn't be necessary
    const jsonPaths = JSON.parse(this.props.paths);
    const searchTitle = jsonPaths.searchTitle;
    const sessionId = jsonPaths.sessionId;

    try {
      const responseStatus = await axios.get(WikiRestApi.urlStatus(searchTitle, sessionId));
      console.log(":::::::::: done with status wait (searchtitle: "
        + searchTitle + " sessionId: " + sessionId + " )::::::::");

      const statusJson = responseStatus.data;

      if (isDoneLoading(statusJson.x, statusJson.y))
      {
        this.props.onLoadingChange(false);
        this.props.onTitleSearch(searchTitle, false);
      }

      let prettyPrintDate = new Date().toLocaleString(
        {hour: 'numeric', minute: 'numeric', second : 'numeric'}
      );
      this.setState({
        messages: [
          "Chill out, we are still working!",
          "Processing: " +  statusJson['x'] + " pages out approx. "+ statusJson['y'],
          "last check at: " + prettyPrintDate
        ]
      });
    }
    catch (err){
      // do nothing
    }

  }

  render() {
    if(this.props.isLoading)
    {
      const listMessages = this.state.messages.map((message, index) =>
        <p key={index}>
          {message}
        </p>
      );
      return (
        <div>
          <img src={loading} className="App-logo" alt="loading-spinner" />
          <div>{listMessages}</div>
        </div>
      );
    }
    else{
      return null;
    }
  }
}

function isDoneLoading(x, y)
{
  return parseInt(x, 10) / parseInt(y, 10) >= 1;
}


export default Loading;
