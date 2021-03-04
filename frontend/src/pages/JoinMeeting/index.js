import "../styles.css"
import React, {useContext, useState,} from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import joinMeetingApiCall from "../../api/joinMeeting"
import userContext from "../../contexts/user-context";

export default function JoinMeeting(){
    const history = useHistory()
    /*const location = useLocation()
    const props = location.state*/

    const [formEntries, setFormEntries] = useState({
        meetingcode: "",
        username:"",
        anonymous: false
    })

    function inputHandler(entryObj){
        let tmpForm = formEntries
        let value = entryObj.target.value
        let name = entryObj.target.name
        
        if(name=="anonymous"){
            tmpForm[name] = (entryObj.target.checked?1:0).toString()
        }else{
            tmpForm[name] = value
        }

        setFormEntries(tmpForm)
    }

    function join(){
        if(formEntries.username=="" || formEntries.meetingcode==""){
            console.log("Enter a meeting code and username")
            return
        }
        console.log(formEntries)
        
        joinMeetingApiCall(formEntries).then(res=>{
            console.log(res)
            history.push({
                pathname: "/AttendeeMeeting",
                state:{
                  meetingdetails:res
                }
            })
        }).catch(err=>{
            console.log(err.message)
            //todo add some kind of error message
        })
        
       
    }

    return(
        <div className="wrap">
        <h1>Find a Meeting</h1>
            <div className="row">
                <input type="text" className="form-control" id="name" name="meetingcode" required onChange={inputHandler}/> 
                <label htmlFor="name">Meeting Code</label>
            </div>

            <div className="row">
                <input type="text" className="form-control" id="name" name="username" required onChange={inputHandler}/> 
                <label htmlFor="name">Username</label>
            </div>
            
            <span><a id="AnonymousMessage">Remain Anonymous</a></span>
            <input type="checkbox" id="Anonymous" name="anonymous" onChange={inputHandler}/>

            
            
            <div>
                <button type="submit" className="green_button" onClick={join}>Join</button>
            </div>
            

    </div>
    )
}