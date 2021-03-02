import "../styles.css"
import React, {useContext, useState,} from 'react';
import { useHistory } from 'react-router-dom';
import joinMeetingApiCall from "../../api/joinMeeting"

export default function JoinMeeting(){
    const history = useHistory()

    const [formEntries, setFormEntries] = useState({
        meetingCode: "",
        companyID:-0,
        username:"",
        anonymous: false
    })

    function inputHandler(entryObj){
        let tmpForm = formEntries
        let value = entryObj.target.value
        let name = entryObj.target.name
        
        if(name=="anonymous"){
            tmpForm[name] = entryObj.target.checked
        }else{
            tmpForm[name] = value
        }

        console.log(tmpForm)
    }

    function join(){
        /*
        joinMeetingApiCall(formEntries).then(res=>{
            history.push({
                pathname: "/AttendeeMeeting",
                state:{
                  event: props.template
                }
            })
        }).catch(err=>{
            //todo add some kind of error message
        })
        */
       console.log(formEntries)
    }

    return(
        <div className="wrap">
        <h1>Find a Meeting</h1>
            <div className="row">
                <input type="text" className="form-control" id="name" name="meetingCode" required onChange={inputHandler}/> 
                <label htmlFor="name">Meeting Code</label>
            </div>

            <div className="row">
                <input type="text" className="form-control" id="name" name="username" required onChange={inputHandler}/> 
                <label htmlFor="name">Username</label>
            </div>
            
            <span><a id="AnonymousMessage">Remain Anonymous</a></span>
            <input type="checkbox" id="Anonymous" name="anonymous" onChange={inputHandler}/>

            
            
            <div>
                <button type="submit" className="green_button">Join</button>
            </div>
            

    </div>
    )
}