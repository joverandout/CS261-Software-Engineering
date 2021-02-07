import React from 'react';
//import { Switch, Route } from 'react-router-dom';
import { Switch, Route } from 'react-router-dom';
//import Route from './route';


import SignIn from '../pages/HostSignIn';
import Timetable from '../pages/Timetable';
import FindMeeting from '../pages/m/FindMeeting';



export default function Routes() {

  const  isPrivate = true
  return (
    <Switch>
      <Route path="/" exact>
        <SignIn/>
      </Route>
      
      <Route path="/Timetable" exact>
        <Timetable/>
      </Route>
      
      <Route path="/FindMeeting" exact>
        <FindMeeting/>
      </Route>   
  
    </Switch>
  );
}