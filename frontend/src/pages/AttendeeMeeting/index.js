import "../styles.css"

import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import x2 from "./x2.png";
import EmotionButton from "../../components/emotion_button"

export default function AttendeeMeeting(){
    const location = useLocation();
    const eList = [["Proud", "#F4b72f"],["Excited","#F4b72f"],["Interested", "#F4b72f"], ["Happy", "#F4b72f"], ["Joyful", "#F4b72f"], ["Optimistic", "#75C7E3"], ["Tired", "#75C7E3"], ["Calm", "#75C7E3"], ["Grateful", "#75C7E3"], ["Bored", "#75C7E3"], ["Sad", "#9B75E3"], ["Insecure", "#9B75E3"], ["Depressed", "#9B75E3"], ["Anxious", "#9B75E3"], ["Afraid", "#9B75E3"], ["Annoyed", "#F07A7A"], ["Angry", "#F07A7A"], ["Overwhelmed", "#F07A7A"], ["Stressed", "#F07A7A"], ["Frustrated", "#F07A7A"]];

    let tmpEmValues = []
    let emotionButtons = []
    for(let i=0; i<eList.length;i++){
        tmpEmValues.push(false)
        let emotionObj={
            name: eList[i][0],
            color: eList[i][1]
        }
        emotionButtons.push(<EmotionButton toggleEmotionCb={toggleEmotionCb} emotion={emotionObj} key={i} id={i}/>)
         
    }
    const [emotionValues, setEmValues] = useState(tmpEmValues)
    function toggleEmotionCb(id, value){
        console.log(value)
        let count = 0
        for(let i=0;i<emotionValues.length;i++){
            if(emotionValues[i] == true){
                count++;
            }
            if(count>=8 && value==true){
                //todo make some kind of popup appear
                console.log("too many emotions selected")
                return false
            }
        }
        let tmpEmValues = emotionValues;
        let val = emotionValues[id]
        tmpEmValues[id] = (val?false:true)
        setEmValues(tmpEmValues)
        return true
    }

    function togglePopup(){

    }

    function issueButton(buttonObj){

    }

    let technicalIssue = (
        <div  id="reportIssue">
        <div className="form-container report-container">
        <button onClick = {togglePopup} className="exit"><img src={x2} /> </button>
        <h1>Report an issue</h1>
        <button className="btn report" onClick={issueButton}>The speaker is too quiet</button>
        <button className="btn report" onClick={issueButton}>The speaker is on mute</button>
        <button className="btn report" onClick={issueButton}>The content is missing</button>
        <div className="row">
            <input type="text" className="form-control" id="name" name="Issue"/> 
            <label htmlFor="name">Report other issue</label>
            <button className="btn report">Send</button>
        </div>
        </div>
    </div>
    )

    let page =(
        <div>
            <div className="header">
                    <h1>Event Name</h1>
            </div>
            <hr/>
            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>
            <hr/>
            <div className="row">
                <input type="text" className="form-control" id="name" name="Feedback"/> 
                <label htmlFor="name">Provide Feedback</label>
            </div>
            <button className="green_button">Send</button>
        </div>
    )

    return(
    <div>
        {page}
    </div>
    )
}