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
           console.log(plot)
           
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
    console.log(location.state)
    const initialState ={
        semanticData: {
            sum:0,
            count:0,
            plot:[[Date.parse(Date()), 0]]
        }
    }
    const [state, dispatch] = useReducer(reducer, initialState)
    const [buttonColour, setButtonColour] = useState("green_button")

    useEffect(()=>{
      const socket = io("http://127.0.0.1:5000", {
        auth:{
          token:"id01043"
        }
      })
      socket.on("feedback", newFeedback)
      return ()=>{
        socket.close()
        console.log("closing")
      }
    },[])
    
    function newFeedback(data){
       dispatch({
           type:"newSemantic",
           semanticValue:data.semantics
       })
       console.log(data)
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

      const page = (
        <div>
          <div>
              <h1>{event.MeetingName}</h1>            
          </div>
          <hr/>
          <div class="row">
            <div class="column">
              <p>Attendees are saying:</p>
              <div class="errorBox">Error goes here and here is a really really long error message to prove if it goes onto a second line</div>
            </div>
            <div class="column">
              <p>Most attendees are:</p>
              <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                  <button>2 or 3 emotion buttons, same as template page</button>
              </div>
            </div>
          </div>
          <div>
              <p>Overall mood graph:</p>
              {lineChart}
          </div>

        </div>
        
      )

    return page
}

