import React, { Component } from 'react';

class WikiSearchForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: '',
      paths: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({title: event.target.value});
  }

  async handleSubmit(event) {
    event.preventDefault();
    this.props.onTitleSearch(this.state.title, true);
  }

  render() {
    return (
      <div name = "WikiSearchForm-div">
        <form onSubmit={this.handleSubmit}>
          <label>
            Wikipedia Title Search:
            <input type="text" value={this.state.title} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}

export default WikiSearchForm;
