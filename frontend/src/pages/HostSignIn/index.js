
import React, {useContext, useState, useCallback} from 'react';
import { Link, useHistory } from 'react-router-dom';

import "../styles.css"
import hostLogIn from "../../api/hostLogIn"

import UserContext from '../../contexts/user-context'

export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);
  const [username, setUsrname] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(null)

  const history = useHistory();
  //In reality we should check if there is already a user logged in to set this

  let contextUser = useContext(UserContext)
  //todo, uncomment this and make sure the user gets added to the context
  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);

  function login(){
    let data={
      username: username,
      password: password
    }
    hostLogIn(data).then(hostid=>{

      contextUser.setUser({
        "Name":username,
        "hostid":hostid
      })
      history.push('/Timetable')
    }).catch(err=>{
      console.log("Could not log in, make sure credentials are valid")
      setError(<p style={{color:"red"}}>Could not log in, make sure credentials are valid</p>)
    })
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

                {error}
                
            </form>
            
            <div>
                    <button onClick={login} className="green_button">GO</button>
              </div>
        </div>

  )
  return page
}