
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

  function pdfClicked(){
    console.log("!!!")
    meetingView({meetingid:event.MeetingID.toString()}).then(b64=>{
      let uri = "data:application/pdf;base64,"+b64

      //stolen code https://stackoverflow.com/questions/2805330/opening-pdf-string-in-new-window-with-javascript
      var byteCharacters = atob(b64);
      var byteNumbers = new Array(byteCharacters.length);
      for (var i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      var byteArray = new Uint8Array(byteNumbers);
      var file = new Blob([byteArray], { type: 'application/pdf;base64' });
      var fileURL = URL.createObjectURL(file);
      window.open(fileURL,"_blank");

    }).catch(err=>{
      console.log(err.message)
    })
  }
  let style = {backgroundColor: "#F2DFA7"}
  let bjsx = (<button style={style} onClick={clicked}>{eventName} | {eventTime} | {tag}</button>)
  
  if(startTimeDate < timeNow.getTime()){
    style = {backgroundColor: "#e7e6e6"}
    console.log("!!!!!!!")
    bjsx = (<button style={style} onClick={pdfClicked}>{eventName} | {eventTime} | {tag}</button>)
  }
  

  


  return(
    <div>
        {bjsx}
    </div>
    
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
        //add the categories to the option list
        let tmpTagOptions = []
        tagList.forEach((tag, index) => {
          tmpTagOptions.push(<option key={index}> {tag} </option>)
        });
        setTagOptions(tmpTagOptions)
        
        //add buttons for all of the events
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
   
  }, [])

  function createEvent(){
    history.push("/CreateEvent")
  }
  
  function logout(){
    history.push("/")
  }
  //display the appropriate events when a category is selected
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

  function createTemplate(){ // we no longer have a create template button on the page
    history.push("/CreateTemplate")
  }
  
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

    </div>

      <hr/>
      <div className="new-btn-group" id="buttons" >
            {/** generated buttons go here*/}
            {eventButtons}
        </div>

    </div>
  );
}