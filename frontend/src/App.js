import logo from './logo.svg';
import { Router } from 'react-router-dom';

import history from './services/history';
import Routes from './routes';

import './App.css';
import ReactDOM from 'react-dom';
function App() {
  return (
    ReactDOM.render(
      <Router history={history}>
          <Routes />
      </Router>
    )
  );
}

export default App;
