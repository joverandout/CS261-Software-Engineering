import React, {useContext} from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import UserContext from '../contexts/user-context'

import SignIn from '../pages/HostSignIn';
import Timetable from '../pages/Timetable';
import PublishEvent from '../pages/PublishEvent';
import CreateEvent from '../pages/CreateEvent';
import CreateTemplate from '../pages/CreateTemplate';
import EosFeedback from '../pages/EosFeedback';
import JoinMeeting from '../pages/JoinMeeting';
import AttendeeMeeting from '../pages/AttendeeMeeting';
import HostMeeting from '../pages/HostMeeting';
import CodeDisplay from '../pages/CodeDisplay';


export default function Routes() {
  //todo make the relevant routes private
  const  isPrivate = true
  //define all of the routes for the application
  return (
    <Switch> 
      <Route path="/" exact>
        <SignIn/>
      </Route>
      
      <PrivateRoute path="/Timetable" exact>
        <Timetable/>
      </PrivateRoute>

      <PrivateRoute path="/PublishEvent" exact>
        <PublishEvent/>
      </PrivateRoute>

      <PrivateRoute path="/CreateEvent" exact>
        <CreateEvent/>
      </PrivateRoute>

      <PrivateRoute path="/CreateTemplate" exact>
        <CreateTemplate/>
      </PrivateRoute>

      <Route path="/EosFeedback" exact>
        <EosFeedback/>
      </Route>

      <Route path="/JoinMeeting" exact>
        <JoinMeeting/>
      </Route>

      <Route path="/AttendeeMeeting" exact>
        <AttendeeMeeting/>
      </Route>

      <PrivateRoute path="/HostMeeting" exact>
        <HostMeeting/>
      </PrivateRoute>

      <PrivateRoute path="/CodeDisplay" exact>
        <CodeDisplay/>
      </PrivateRoute>

  
    </Switch>
  );
}

function PrivateRoute({ children, ...rest }) {
  //used when user infromation is required for a page to function
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