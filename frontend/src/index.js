import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { Router } from 'react-router-dom';
import history from './services/history';
import Routes from './routes';

const UserContext = React.createContext(null) // initiall no user

const routing = (
  <Router history={history}>
      <Routes />
  </Router>
)

ReactDOM.render(
  routing,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
