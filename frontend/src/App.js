import { Router } from 'react-router-dom';
import Routes from './routes';

import './App.css';
import React, { useState } from 'react';

import UserContext from './contexts/user-context'

//entry point for the application
export default function App() {
  const [userC, setUserC] = useState({
    user:null,
    setUser:setUserFunction
  });

  function setUserFunction(newUser){
    setUserC({
      user: newUser,
      setUser: setUserFunction
    })
  }

  return (
    <UserContext.Provider value={userC}>
      <Routes />
    </UserContext.Provider >
  );
}


