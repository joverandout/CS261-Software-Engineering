import "../styles.css"
import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import startMeeting from "../../api/startMeeting";

export default function PublishEvent(){
    let location = useLocation()
    const history = useHistory();
    //todo, add error checking here in case the state doesnt exist
    const event = location.state.event
    const eventName = event.MeetingName
    const startTime = event.StartTime

    //tell the server to start the event
    function startEvent(){

        startMeeting({meetingid:event.MeetingID.toString()}).then(res=>{
            event.MeetingCode = res
            history.push({
                pathname: "/CodeDisplay",
                state:{
                    event:event
                }
            })
        }).catch(err=>{
            console.log(err.message)
        })
       
    }

    function backButton(){
        history.push({
            pathname: "/Timetable"
          })
    }

    //todo add qrcode

    //todo add periodic checks for when the time starts
    // to be honest for the purpose of the demo we can just have everything set to some early time thats already passed
    /*
    let startButton = (null)
    if(Date.parse(Date())>Date.parse(startTime)){
        startButton = (
            <div>
                <button className="green_button" onClick={startEvent}>Start Event</button>
            </div>
        ) 
    }*/
    let startButton = (
        <div>
            <button className="green_button" onClick={startEvent}>Start Event</button>
        </div>
    ) 
    return (
        
        <div>
            <button className="white_button" id="back_button" onClick={backButton}>Back</button>
            <div className="header">
                <h1>Publish Event</h1>
            </div>
            <hr/>
            <div className="wrap">

                    <br/>

                    <p>Do you want to start the following event?</p><br/>
                    <p style={{fontSize: "xx-large"}}>{eventName}</p> 
                    <br/><p>Scheduled for: {startTime}</p><br/>

                    {startButton}
            </div>
        </div>
    );
}