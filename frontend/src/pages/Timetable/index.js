
import React, { useState, useEffect, useContext } from 'react';
import { Link, useHistory } from 'react-router-dom';
import "../styles.css";

import getHostMeetings from "../../api/getHostMeetings"
import UserContext from '../../contexts/user-context'
import meetingView from '../../api/meetingView';


function EventComponent(props){
  const history = useHistory();
  
  if(!props.event){
    return <p>No event found</p>
  }  

  let event = props.event
  
  let eventName = event.MeetingName
  let eventTime = event.StartTime

  let startTimeDate = Date.parse(event.StartTime)
  let timeNow = new Date()

  let style = {backgroundColor: "#e7e6e6"}

  if(startTimeDate > timeNow.getTime()){
    style = {backgroundColor: "#F2DFA7"}
  }
  
  let tag = event.Category

  function clicked(){
    history.push({
      pathname: "/PublishEvent",
      search:"eventID",
      state:{
        event: props.event
      }
    })
  }
  let style = {backgroundColor: "#e7e6e6"}
  let bjsx = (<button style={style} onClick={clicked}>{eventName} | {eventTime} | {tag}</button>)
  if(startTimeDate > timeNow.getTime()){
    style = {backgroundColor: "#F2DFA7"}
    meetingView.then(res=>{

    }).catch(err=>{
      console.log("No Pdf")
      bjsx = (<button style={style}>{eventName} | {eventTime} | {tag}</button>)
 
    })
    bjsx = (<button style={style} >{eventName} | {eventTime} | {tag}</button>)
  }
  

  


  return(
    {bjsx}
  );
}

export default function Timetable(){
  const [eventButtons, setEventButtons] = useState([])
  const [tagOptions, setTagOptions] = useState([])
  const [eventList, setEventList] = useState([]) // doesnt really need to be a hook tbh
  const [tagList, setTagList] = useState([]) //neither does this

  const history = useHistory()
  const contextUser = useContext(UserContext)
  const [user, setUser] = useState(contextUser.user)
  //Runs once to get the event list form the server.
  useEffect(()=>{
    if(user!=null){
        
        getHostMeetings({hostid:user.hostid.toString()}).then(data=>{
        let tmpEvList = data[0]
        let tagList = data[1]
        setEventList(tmpEvList)
    
        let tmpTagOptions = []
        tagList.forEach((tag, index) => {
          tmpTagOptions.push(<option key={index}> {tag} </option>)
        });
        setTagOptions(tmpTagOptions)
    
        let evButtons = []
        for(let i=0; i<tmpEvList.length; i++){
          evButtons.push(<EventComponent event={tmpEvList[i]} key={i} id={i}/>)
        }
        setEventButtons(evButtons)
      }).catch(err=>{
        console.log(err.message)
        setEventButtons(<h1>No Events Found</h1>)
      })
    }
    
    //todo nake sure this returns as valid

   
  }, [])

  function createEvent(){
    history.push("/CreateEvent")
  }
  
  function logout(){
    history.push("/")
  }

  function refreshEventList(fieldObj){
    let tag = fieldObj.target.value
    
    let evButtons = []
    for(let i=0; i<eventList.length; i++){
      if(tag=="All" || tag==eventList[i].Category){
        evButtons.push(<EventComponent event={eventList[i]} key={i} id={i}/>)
      }  
    }
    setEventButtons(evButtons)
  }

  function createTemplate(){
    history.push("/CreateTemplate")
  }
  // todo - change the username according to the context details
  return(
    <div>
       <button className="white_button" id="back_button" onClick={logout}>Log Out</button>
        <button className="white_button" id="new_event" onClick={createEvent} style={{paddingTop: "5"}}> Create New Event </button>
    
    <div className="wrap">
    
     
        
        <div className="header" id="avoid_buttons">
            <h1>Welcome, {user.Name} </h1>
            <h3>Your scheduled meetings:</h3>
            <p style={{fontSize: 18, fontWeight: "bold", textAlign: "left"}}> Filter by Category: </p>
            <select name="cat" id="cat" style={{width: "30vw", paddingLeft: 10, marginRight: "60vw"}} onChange={refreshEventList}> 
                <option> --Select Category-- </option>
                <option> All </option>
                {tagOptions}
            </select>
        </div>

        <hr/>


                <div className="btn-group" id="buttons" >
                  {/** generated buttons go here*/}
                  {eventButtons}
                </div>

    </div>
    </div>
  );
}