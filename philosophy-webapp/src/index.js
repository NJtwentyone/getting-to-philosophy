import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import GettingToPhilosophy from './GettingToPhilosophy';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<GettingToPhilosophy />, document.getElementById('root'));
registerServiceWorker();
