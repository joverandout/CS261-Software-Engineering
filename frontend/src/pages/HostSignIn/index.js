
import React, {useContext, useState} from 'react';
import { Link } from 'react-router-dom';

import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);
  const [nextbutton, setButton] = useState(null);
  let contextUser = useContext(UserContext)
  console.log(contextUser)



  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);
  const button = (
    <Link to="/Timetable">
    <button>
      Next Page
    </button>
    </Link>
  )

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
                  /*This works becuase updating this hook causes a re-render. 
                  When the route component is rendered it sees that we are now 
                  signed in

                  This is OK becuase there aren't usually sign in and "next" buttons.. Just one
                  plus we need to get confirmation from the server before setting the hook
                  */
                  name:'Nkosi',
                  id:1
                })
                setButton(button)
              }else{
                setSignedIn(false);
                setUser(null);
                setButton(null)
              }
            }}>
              Sign In
            </button>
         )
       }
      </UserContext.Consumer>
      {nextbutton}

      

    </div>
  )
  return page
}