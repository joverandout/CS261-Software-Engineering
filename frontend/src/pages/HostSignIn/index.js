
import React, {useContext, useState} from 'react';
import { Link } from 'react-router-dom';

import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);

  let contextUser = useContext(UserContext)
  console.log(contextUser)



  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);

  const page = (
    <div>
      <h1>Host Sign In Page</h1>
      {signedInIndicator}

      {/* This code is remarkably ugly... idek if its possible to put the function elsewhere
      But context relies on "function as a child" */}

      <UserContext.Consumer>
       {
         ({user, setUser})=>(
            <button onClick={()=>{

              if(signedIn == false){
                setSignedIn(true);
                setUser({ 
                  name:'Nkosi',
                  id:1
                })
                
              }else{
                setSignedIn(false);
                setUser(null);
                
              }
            }}>
              Sign In
            </button>
         )
       }
      </UserContext.Consumer>

      <Link to="/Timetable">
      <button>
        Next Page
      </button>
    </Link>
      

    </div>
  )
  return page
}