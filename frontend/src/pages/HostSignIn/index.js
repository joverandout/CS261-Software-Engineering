
import React, {useContext, useState, useCallback} from 'react';
import { Link, useHistory } from 'react-router-dom';
import Axios from 'axios';

import "../styles.css"




import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);
  const [username, setUsrname] = useState("")
  const [password, setPassword] = useState("")

  const history = useHistory();
  //In reality we should check if there is already a user logged in to set this

  let contextUser = useContext(UserContext)
  //todo, uncomment this and make sure the user gets added to the context
  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);
  function login(){
    /*
    Axios.post("http://127.0.0.1:5000/login",{
      "username":username,
	    "password":password
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
      history.push('/Timetable')
      
    }).catch(err => {

      //console.log(err)
      console.log(err)
      setSignedIn(false)
      contextUser.setUser({
        user:null,
        setUser:contextUser.setUser
      })
    })
    */
   history.push('/Timetable')
  }

  function usernameChange(e){
    setUsrname(e.target.value)

    
  }

  function passwordChange(e){
    setPassword(e.target.value)
    
  }

  const page = (

        <div className="wrap">
            <h1>Host Login</h1>
            {signedInIndicator}
            <form action=""> 

                <div className="row">
                    <input type="text" className="form-control" onChange={usernameChange}  required/> 
                    <label htmlFor="name">Username</label>
                </div>

                <div className="row">
                    <input type="password"  className="form-control" onChange={passwordChange} required/>
                    <label htmlFor="pw">Password</label>
                </div>
                
                <span className="link">I’ve forgotten my password</span>
                
            </form>
            <div>
                    <button onClick={login} className="green_button">GO</button>
                </div>
        </div>

  )
  return page
}