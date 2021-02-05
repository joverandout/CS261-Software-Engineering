import React from 'react';
//import { Switch, Route } from 'react-router-dom';
import { Switch } from 'react-router-dom';
import Route from './route';


import SignIn from '../pages/HostSignIn';

import Timetable from '../pages/Timetable';

import FindMeeting from '../pages/m/FindMeeting';

export default function Routes() {

  const  isPrivate = true
  return (
    <Switch>
      <Route path="/" exact component={SignIn} />
      
      <Route path="/Timetable" component={Timetable} isPrivate />  
      
      <Route path="/FindMeeting" component={FindMeeting}  />     
      {/* redirect user to SignIn page if route does not exist and user is not authenticated */}
      <Route component={SignIn} />
    </Switch>
  );
}