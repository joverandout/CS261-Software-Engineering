import "../styles.css"
import "./cdstyle.css"
import stopMeeting from "../../api/stopMeeting"
import endMeeting from "../../api/endMeeting"
import qrImage from '../../pages/CodeDisplay/qr.png';

import React, {useReducer, useState, useMemo, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';

export default function CodeDisplay(){
    const location = useLocation()
    const event = location.state.event 
    const history = useHistory()

    // Navigate to the live feedback page
    function goLive(){
        console.log("??")
        history.push({
            pathname: "/HostMeeting",
            state:{
                event:event
            }
        })
    }

    // stop the meeting and go back to the timetable page
    function endEvent(){
        let data = {meetingid:event.MeetingID.toString()}
        endMeeting(data).then(res=>{
            stopMeeting(data).then(res=>{
                history.push("/Timetable")
            }).catch(err=>{
                console.log(err.message)
                history.push("/Timetable")//go back to the timetable place regardless
            })
        }).catch(err=>{
            console.log(err.message)
            history.push("/Timetable")//go back to the timetable place regardless
        })
    }

    return(
        <div>
            <button className="white_button buttonend" id="back_button" onClick={endEvent}>END EVENT</button>
            <button className="yellow_button buttonlive" id="next_button" onClick={goLive}>View Live Feedback</button>
            <div className="header">
                <h1>{event.MeetingName}</h1>
                
            </div>
            <button className="green_button" id="progress_button">In Progress</button>

            <hr/>

            <div className="split left">
                <div className="centered">
                <p className="image">Join this event by scanning the QR code below</p>
                <img src={qrImage} alt="QR Code" ></img>
                </div>
            </div>
            
            <div className="split right">
                <div className="centered vh" >
                    <p> Or go to </p>
                    <p className="bigtext">www.my.meeting.com</p>
                    <p> and enter the meeting code: </p>
                    <p className="bigtext">{event.MeetingCode}</p>  
                </div>
            </div>

            
        </div>
    )
}