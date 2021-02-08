
import React, {useContext, useState} from 'react';
import { Link } from 'react-router-dom';
import Axios from 'axios';

import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);
  //In reality we should check if there is already a user logged in to set this

  let contextUser = useContext(UserContext)
  console.log(contextUser)

  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);

  function login(){
    Axios.post("http://127.0.0.1:5000/login",{
      "username":"Nkosi",
	    "password":"password123"
    }).then(res => {

      console.log(res)
      contextUser.setUser({
        user:{
          "Name":"Nkosi",
          "id":3
        },
        setUser:contextUser.setUser
      })
      setSignedIn(true)
    }).catch(err => {

      console.log(err)
      setSignedIn(false)
      contextUser.setUser({
        user:null,
        setUser:contextUser.setUser
      })
    })
  }

  const page = (
    <div>
      <h1>Host Sign In Page</h1>
      {signedInIndicator}

      <button onClick={login}>
        Sign In
      </button>

      <Link to="/Timetable">
      <button>
        Next Page
      </button>
    </Link>
    </div>
  )
  return page
}