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


export default function Routes() {
  //todo make the relevant routes private
  const  isPrivate = true
  //Special route for the loggin screen?
  return (
    <Switch> 
      <Route path="/" exact>
        <SignIn/>
      </Route>
      
      <Route path="/Timetable" exact>
        <Timetable/>
      </Route>

      <Route path="/PublishEvent" exact>
        <PublishEvent/>
      </Route>

      <Route path="/CreateEvent" exact>
        <CreateEvent/>
      </Route>

      <Route path="/CreateTemplate" exact>
        <CreateTemplate/>
      </Route>

      <Route path="/EosFeedback" exact>
        <EosFeedback/>
      </Route>

      <Route path="/JoinMeeting" exact>
        <JoinMeeting/>
      </Route>

      <Route path="/AttendeeMeeting" exact>
        <AttendeeMeeting/>
      </Route>

      <Route path="/HostMeeting" exact>
        <HostMeeting/>
      </Route>
  
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