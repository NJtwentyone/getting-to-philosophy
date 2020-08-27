import React, { Component } from 'react';
import WikiSearchForm from './WikiSearchForm';
import PathToPhilosophy from './PathToPhilosophy';
import Loading from './Loading';
import logo from './logo.svg';
import './GettingToPhilosophy.css';
import axios from 'axios';
import WikiRestApi from './api/wiki-rest/WikiRestApi'

class GettingToPhilosophy extends Component {
  constructor(props) {
    super(props);
    this.handlePathsChange = this.handlePathsChange.bind(this);
    this.handleLoadingChange = this.handleLoadingChange.bind(this);
    this.handleErrorChange = this.handleErrorChange.bind(this);
    this.handleTitleSearch = this.handleTitleSearch.bind(this);
    this.state = {
      paths: '{}',
      isLoading : false,
      hasErrors : false,
    };
  }

  handlePathsChange(paths) {
  console.log("gtp paths:" + paths);
    this.setState({paths: paths});

    //if no_data -> then fire of urlFind
    // then start loading component
  }

  handleLoadingChange(isLoading) {
  console.log("gtp isLoadig:" + isLoading);
    this.setState({isLoading: isLoading});
  }

  handleTitleChange(title) {
  console.log("gtp title:" + title);
    this.setState({title: title});
  }

  handleErrorChange(hasErrors) {
  console.log("gtp hasErrors:" + hasErrors);
    this.setState({hasErrors: hasErrors});
  }

  async handleTitleSearch(title, startFind) {
    var hasErrors = false;
    var continueToFind = false;
    try {
      // NOTE return should be quick, no need for loading UI here
      const responsePath = await axios.get(WikiRestApi.urlPath(title));
      this.handlePathsChange(JSON.stringify(responsePath.data));
      const jsonPaths = responsePath.data;
      hasErrors = 'errors' in jsonPaths;
      continueToFind = jsonPaths['status'] === 'no_data';
    }
    catch(err)
    {
      this.handleErrorChange(true);
      console.log(err);
    }

    if(hasErrors) {
      this.handleErrorChange(true);
    }

    if(!continueToFind || hasErrors || !startFind)
    {
      return;
    }

    this.handleLoadingChange(true);

    try {
      // NOTE: start process to find path
      const responseFind = await axios.get(WikiRestApi.urlFind(title));
      console.log(":::::::::: done with find wait::::::::");

      this.handlePathsChange(JSON.stringify(responseFind.data));
    }
    catch (err){
      // do nothing
      this.handleErrorChange(true);
      console.log(err);
    }

  }

  render() {
    const paths = this.state.paths;

    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Getting to Philosophy</h1>
        </header>
        <WikiSearchForm
          onPathsChange={this.handlePathsChange}
          onLoadingChange={this.handleLoadingChange}
          onErrorChange={this.handleErrorChange}
          onTitleSearch={this.handleTitleSearch}/>

        <PathToPhilosophy
          paths={paths}
          isLoading={this.state.isLoading} />

        <Loading
          paths={paths}
          isLoading={this.state.isLoading}
          onLoadingChange={this.handleLoadingChange}
          onTitleSearch={this.handleTitleSearch} />
      </div>
    );
  }
}

export default GettingToPhilosophy;
