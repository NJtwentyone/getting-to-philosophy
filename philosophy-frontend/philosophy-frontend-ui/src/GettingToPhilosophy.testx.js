import React from 'react';
import ReactDOM from 'react-dom';
import GettingToPhilosophy from './GettingToPhilosophy';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<GettingToPhilosophy />, div);
  ReactDOM.unmountComponentAtNode(div);
});
