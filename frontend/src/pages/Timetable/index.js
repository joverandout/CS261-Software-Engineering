
import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import "../styles.css";

import getHostMeetings from "../../api/getHostMeetings"

function EventComponent(props){
  const history = useHistory();
  
  if(!props.event){
    return <p>No event found</p>
  }

  let event = props.event
  let eventName = event.eventName
  let eventTime = event.eventTime
  let tag = event.tag

  function clicked(){
    history.push({
      pathname: "/PublishEvent",
      search:"eventID",
      state:{
        event: props.event
      }
    })
  }


  return(
    <button onClick={clicked}>{eventName} {eventTime} {tag}</button>
  );
}

export default function Timetable(){
  const [eventsRefreshed, setEvRefresh] = useState(false); //only change this if we need to ask for the list of events again for some reason
  const [eventButtons, setEventButtons] = useState([])
  

  useEffect(()=>{
    
    let eventList = getHostMeetings()
    let evButtons = []
    for(let i=0; i<eventList.length; i++){
      evButtons.push(<EventComponent event={eventList[i]} key={i} id={i}/>)
    }
    setEventButtons(evButtons)
    
  }, [eventsRefreshed])

  
  // todo - change the username according to the context details
  // todo - add facility for no events
  return(
    <div>
       <button className="white_button" id="back_button" >Log Out</button>
        <button className="white_button" id="new_event" > Create New Event </button>
    
    <div className="wrap">
     
        
        <div className="header" id="avoid_buttons">
            <h1>Welcome, Username </h1>
            <h3>Your scheduled meetings:</h3>
            <p style={{fontSize: 18, fontWeight: "bold", textAlign: "left"}}> Filter by Category: </p>
            <select name="cat" id="cat" style={{width: "30vw", paddingLeft: 10, marginRight: "60vw"}}> 
                <option> --Select Category-- </option>
            </select>
        </div>

        <hr/>


                <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                  {/** generated buttons go here*/}
                  {eventButtons}
                </div>

    </div>
    </div>
  );
}