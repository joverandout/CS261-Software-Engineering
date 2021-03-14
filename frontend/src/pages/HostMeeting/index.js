import "../styles.css"
import "./cdstyle.css"
import React, {useReducer, useState, useMemo, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import { Chart } from "react-charts"
import {io, Socket} from "socket.io-client"
import endMeeting from "../../api/endMeeting"
import stopMeeting from "../../api/stopMeeting"
import hostLogIn from "../../api/hostLogIn";

function reducer(state, action){
    switch(action.type){
        case "newSemantic": // update the rollong average and plot data when new feedback is received
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
 
    const [textFeedback, setTextFeedback] = useState([])
    const [emotions, setEmotions] = useState([])

    const [emotionElements, setEmotionElements] = useState([])
    
    const [technicalFeedback, setTechnicalFeedback] = useState([])

    useEffect(()=>{

      let sortable = emotions
      //sort the emotions from highest to lowest represented
      sortable.sort((a,b)=>{
        return b[1] - a[1];
      })
      let elements = []

      for(let i=0;i<sortable.length;i++){
        if(i>2){ // only display 3 emotions
          break
        }
        let p = sortable.length-i
        
        elements.push(<p key={i}>{sortable[i][0]} - {sortable[i][1]}</p>)
      }
      setEmotionElements([...elements])
    },[emotions])

    //connect to the socket when the page loads
    useEffect(()=>{
      const socket = io("http://127.0.0.1:5000", {
        auth:{
          token:"id01043"
        }
      })

      socket.on("feedback", newFeedback)
      return ()=>{
        socket.close()
        console.log("closing socket")
      }
      
    },[])
    

    function newFeedback(data){
        console.log(data)
        if(data.emotion || data.Technical){ //check if it's technical feedback that we have received
          setTechnicalFeedback(data.Technical)
          return 
        }
        console.log(data)
        dispatch({
           type:"newSemantic",
           semanticValue:data.semantics
           
        })
        // if we recieved text feedback, add it to the box to be displayed
        if(!(data.generalText == "")){
          let feedback = textFeedback
          feedback.push((<p key={textFeedback.length}>{data.generaltext}</p>))
          setTextFeedback([...feedback] )
        }
        console.log(data.emotions, data.ratings)
        let tmpEmotions = emotions
        
        if(tmpEmotions.length==0){
          data.emotions.forEach((element,i) => {
            tmpEmotions.push([element, parseInt(data.ratings[i])]) //initialise the array if this is the first time
          });
        }else{
          tmpEmotions.forEach((element,i) => {
            tmpEmotions[i][1]+=parseInt(data.ratings[i])//otherwise simply update the array
          });
        }
        console.log(tmpEmotions)
        setEmotions([...tmpEmotions])
    }
    //signal the end of the meeting to cause the end of session feedback to display
    function triggerEnd(){
      let data = {"meetingid":event.MeetingID.toString()}
      endMeeting(data).then(res=>{
        stopMeeting(data).catch(err=>{
          console.log(err.message)
        })
      }).catch(err=>{
        console.log(err.message)
      })
      history.push("/Timetable")
    }

    // define the properties of the chart
    const data = useMemo(
        () => [
          {
            label: 'Feedback Positivity',
            data: state.semanticData.plot
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

        <div
          style={{
            width: '1000px',
            height: '700px'
          }}
        >
          <Chart data={data} axes={axes} />
        </div>
      )
      

    return(
      <div>
          <div className="mybtn-group">
          <button className="white_button buttonend" onClick={triggerEnd}>END EVENT</button>
            <button className="yellow_button" style={{padding:"24px"}} onClick={()=>{history.goBack()}}>View Meeting Code</button>
            <h1>{event.MeetingName}</h1>   
            <button className="green_button buttonlive" >In Progress</button>
          </div>
          <hr/>
          <div className="row">
            <div className="column">
            <div className="errorBox" onClick={()=>{setTechnicalFeedback("")}}>{technicalFeedback}</div>
              <br></br>
              <h3>Attendees are saying:</h3>
              <div className="scrollable">
                {textFeedback}
              </div>
            </div>
            <div className="column">
              <h3>Attendees are feeling:</h3>
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

