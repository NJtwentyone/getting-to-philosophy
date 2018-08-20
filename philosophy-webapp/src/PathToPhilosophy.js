import React, { Component } from 'react';

import {isEmpty} from './lib/jsonUtils';
import PathVisualize from './PathVisualize'

class PathToPhilosophy extends Component {

  render() {

    const jsonPaths = JSON.parse(this.props.paths);
    const isJsonEmpty = isEmpty(jsonPaths)
    const hasData = !isJsonEmpty && jsonPaths['status'] === 'data'
    const hasErrors = !isJsonEmpty && ('errors' in jsonPaths)

    return (
    <div>
      <PathTitle
        title={jsonPaths.searchTitle}
        hasData={hasData}
        hasErrors={hasErrors}/>
      <PathVisualize
        jsonPathTitles={jsonPaths.pathTitles}
        isLoading={this.props.isLoading} />
    </div>
    );
  }
}

function PathTitle(props) {
  if(!props.title){
    return <h1>&nbsp;</h1>;
  }
  else if(props.hasData) {
    return <h1>Title: {props.title}</h1>;
  }
  else if(props.hasErrors) {
    return <h1>Title: &quot;{props.title}&quot; not found </h1>;
  }
  return null;
}

export default PathToPhilosophy;
