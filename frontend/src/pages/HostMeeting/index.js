import "../styles.css"
import "./cdstyle.css"
import React, {useReducer, useState, useMemo, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import { Chart } from "react-charts"
import {io} from "socket.io-client"
import endMeeting from "../../api/endMeeting"
import stopMeeting from "../../api/stopMeeting"
import hostLogIn from "../../api/hostLogIn";

function reducer(state, action){
    switch(action.type){
        case "newSemantic":
            let currentSum = state.semanticData.sum
            let currentCount = state.semanticData.count
            let actionVal = action.semanticValue

           let newCount = currentCount+1
           let newSum = currentSum+actionVal
           let ave = newSum/newCount
           let plot = [...state.semanticData.plot, [Date.parse(Date()), ave]]
           
           return {
               semanticData:{
                   sum:newSum,
                   count:newCount,
                   plot:plot
               }
           }
    }
}

export default function HostMeeting(){
    const location = useLocation()
    const history = useHistory()
    const event = location.state.event

    const initialState ={
        semanticData: {
            sum:0,
            count:0,
            plot:[[Date.parse(Date()), 0]]
        }
    } 
    const [state, dispatch] = useReducer(reducer, initialState)
    const [buttonColour, setButtonColour] = useState("green_button")
    
    const [textFeedback, setTextFeedback] = useState([])
    const [emotions, setEmotions] = useState([])

    const [emotionElements, setEmotionElements] = useState([])
    
    const [technicalFeedback, setTechnicalFeedback] = useState([])

    useEffect(()=>{

      let sortable = emotions
      
      sortable.sort((a,b)=>{
        return a[1] - b[1];
      })
      let elements = []

      for(let i=0;i<sortable.length;i++){
        if(i>3){
          break
        }
        let p = sortable.length
        elements.push(<p key={i}>{sortable[i][0]} - {sortable[i][1]}</p>)
      }
      setEmotionElements([...elements])
      console.log("!!!!")
    },[emotions])
    
    function newFeedback(data){

        if(data.emotion){
          setTechnicalFeedback(data.generalText)
          return 
        }

        dispatch({
           type:"newSemantic",
           semanticValue:data.semantics
        })
       
        if(!(data.generalText == "")){
          let feedback = textFeedback
          feedback.push((<p key={textFeedback.length}>{data.generaltext}</p>))
          setTextFeedback([...feedback] )
        }
        console.log(data.emotions, data.ratings)
        let tmpEmotions = emotions
        
        if(tmpEmotions.length==0){
          data.emotions.forEach((element,i) => {
            tmpEmotions.push([element, parseInt(data.ratings[i])])
          });
        }else{
          tmpEmotions.forEach((element,i) => {
            tmpEmotions[i][1]+=parseInt(data.ratings[i])
          });
        }
        console.log(tmpEmotions)
        setEmotions([...tmpEmotions])
    }

    function triggerEnd(){
      let data = {"meetingid":event.MeetingID.toString()}
      if(buttonColour == "green_button"){
        endMeeting(data).then(res=>{
          setButtonColour("yellow_button")
        }).catch(err=>{
          console.log("Could not end the meeting")
        })
      }else{
        stopMeeting(data).then(res=>{
          history.push("/Timetable")
        }).catch(err=>{
          console.log("Could not stop the meeting")
          history.push("/Timetable")
        })
      }
    }

    const data = useMemo(
        () => [
          {
            label: 'Series 1',
            data: state.semanticData.plot//[[0,0],[1,1],[2,1],[3,-1]]
          }
        ]
      )
     
      const axes = useMemo(
        () => [
          { primary: true, type: 'utc', position: 'bottom' },
          { type: 'linear', position: 'left' }
        ],
        []
      )
     
      const lineChart = (
        // A react-chart hyper-responsively and continuously fills the available
        // space of its parent element automatically
        <div
          style={{
            width: '900px',
            height: '700px'
          }}
        >
          <Chart data={data} axes={axes} />
        </div>
      )
      

    return(
      <div>
          <div class="mybtn-group">
          <button className="white_button buttonend" onChange={triggerEnd}>END EVENT</button>
            <button className="yellow_button" style={{padding:"24px"}} onChange={()=>{history.goBack()}}>View Meeting Code</button>
            <h1>{event.MeetingName}</h1>   
            <button className="green_button buttonlive" >In Progress</button>
          </div>
          <hr/>
          <div className="row">
            <div className="column">
            <div className="errorBox">Error goes here and here is a really really long error message to prove if it goes onto a second line</div>
              <br></br>
              <h3>Attendees are saying:</h3>
              <div className="scrollable">
                {textFeedback}
              </div>
            </div>
            <div className="column">
              <h3>Most attendees are:</h3>
              <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                  
                  {emotionElements}
              </div>
            </div>
          </div>
          <div className="graph">
              <h3>Overall mood graph:</h3>
              {lineChart}
          </div>

        </div>
    )
}

