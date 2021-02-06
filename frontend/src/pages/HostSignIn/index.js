
import React, {useState} from 'react';
import { Redirect } from 'react-router-dom';
import userContext from '../../contexts/user-context';
import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);

  function signin(){
    setSignedIn(signedIn != true);
  }

  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);

  const page = (
    <div>
      <h1>Host Sign In Page</h1>
      {signedInIndicator}

      {/* This code is remarkably ugly... idek if its possible to put the function elsewhere
      But context relies on "function as a child" */}
      <button onClick={signin}>
        Sign In
      </button>
      <UserContext.Consumer>
       {
         ({user, setUser})=>(
            <button onClick={()=>{
              console.log(user)
              if(signedIn == true){
                setUser({
                  name:'Nkosi',
                  id:1
                })
              }else{
                setUser(null)
              }
            }}>
              Next
            </button>
         )
       }
      </UserContext.Consumer>

      

    </div>
  )
  return page
}