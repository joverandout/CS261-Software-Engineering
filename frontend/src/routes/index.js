import React, {useContext} from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import UserContext from '../contexts/user-context'

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
      
      <PrivateRoute path="/Timetable" exact>
        <Timetable/>
      </PrivateRoute>
      
      <PrivateRoute path="/FindMeeting" exact>
        <FindMeeting/>
      </PrivateRoute>   
  
    </Switch>
  );
}

function PrivateRoute({ children, ...rest }) {

  let contextUser = useContext(UserContext)
  let authorised = false
  if(contextUser.user != null){
    authorised = true
  }

  return (
    <Route {...rest}
      render={({ location }) =>

        authorised ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/",
              state: { from: location }
            }}
          />
        )
      }
    />
  );
}