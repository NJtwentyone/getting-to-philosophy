import React, { Component } from 'react';

import {isEmpty} from './lib/jsonUtils';

class PathVisualize extends Component {

  render() {
    if(!isEmpty(this.props.jsonPathTitles))
    {
      return <PathSimpleDisplay
                paths={this.props.jsonPathTitles} />;
    }
    else if (!this.props.isLoading){
      return <div>'Nothing to show now, Enter in a title'</div>;
    }
    else{
      return <div></div>;
    }
  }
}

function PathSimpleDisplay(props)
{
  // TODO use wiki guid for key
  const listItems = props.paths.map((path, index) =>
    <li key={index}>
      {path}
    </li>
  );
  return (
    <div>
      <h2>Total Hops: {props.paths.length - 1}</h2>
      <ol>{listItems}</ol>
    </div>
  );
}


export default PathVisualize;
