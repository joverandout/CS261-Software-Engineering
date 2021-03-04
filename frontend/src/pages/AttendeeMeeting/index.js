import "../styles.css"
import "./popup_styles.css"

import React, {useContext, useState, useCallback, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import x2 from "./x2.png";
import EmotionButton from "../../components/emotion_button"
import userFeedback from "../../api/userFeedback"

export default function AttendeeMeeting(){
    const location = useLocation();
    /*const meetingdetails = location.state.meetingdetails
    const template = meetingdetails.template*/
    const meetingdetails = {
        meetingid:1,
        companyid:1,
        template:{
            emotions:["happy", "neutral", "sad"],
            questions:["How was the meeting?", "What are you having for lunch?", "Could you understand?"]
        }
    }
    
    const [emotionButtons, setEmotionButtons] = useState([])
    const [emotionValues, setEmValues] = useState([])
    const [displayElement, setDisplayElement] = useState(0)
    const [lastPressed, setLastPressed] = useState(null)
    const [score, setScore] = useState(0)
    const [popup, setPopup] = useState(false)
    const [feedback, setFeedback] = useState("")

    const [render, setRender] = useState(false)

    useEffect(()=>{
        console.log("Once")
        let tmpEmValues = []
        let tmpEmButtons = []
        meetingdetails.template.emotions.forEach((emotion,i)=>{
            tmpEmValues.push(0)
            tmpEmButtons.push(<EmotionButton name={emotion} toggleEmotionCb={toggleEmotionCb} value={false} id={i} key={i}/>)
        })
        setEmotionButtons(tmpEmButtons)
        setEmValues(tmpEmValues)
        //setDisplayElement(page)
    },[])

    useEffect(()=>{
        console.log("Emotion Values Changed!")
        let tmpEmButtons=[]
        console.log(emotionValues)
        emotionValues.forEach((val,i)=>{
            let value = (val>0)?true:false
            
            let name = meetingdetails.template.emotions[i]
            tmpEmButtons.push(<EmotionButton name={name} toggleEmotionCb={toggleEmotionCb} value={value} id={i} key={i}/>)
        })
        
        setEmotionButtons([...tmpEmButtons])
        setDisplayElement(0)
        
    }, [emotionValues])

    function setEm(values){
        setEmValues([...values])
    }

    function togglePopup(){
        let tmpPopup = popup?false:true 

        if(tmpPopup){
            setDisplayElement(2)
        }else{
            setDisplayElement(0)
        }
        setPopup(tmpPopup)
    }


    

    function issueButton(buttonObj){

    }

    function scoreChange(inObj){
        setScore(inObj.target.value)
    }

    function scoreOk(){
        let tmpEmValues = emotionValues
        tmpEmValues[lastPressed] = parseInt(score)
        setEmValues([...tmpEmValues])
        
        setScore(0)
    }

    function formHandler(formObj){
        setFeedback(formObj.target.value)
        
    }

    function sendFeedback(){
        let emotions = []
        let scores = []
        meetingdetails.template.emotions.forEach((emotion,i)=>{
            emotions.push(emotion)
            scores.push(emotionValues[i].toString())
        })
        let now = new Date()
        let h = now.getHours().toString()
        let m = now.getMinutes().toString()
        let s = now.getSeconds().toString()
        let time = h+":"+m+":"+s
        let data={
            generaltext:feedback,
            meetingid: meetingdetails.meetingid.toString(),
            companyid: meetingdetails.companyid.toString(),
            rating: scores.join(),
            emotion: emotions.join(),
            ftime:time
        
        }
        console.log(data)
        userFeedback(data).then(res=>{
            //refresh all the values
            console.log("Feedback successfully sent")
        }).catch(err=>{
            console.log(err.message)
        })
    }
    
    //todo manage state of components from parent to allow state resetting
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

    
    
    let emotionScore=(
        <div>
            <div className="row">
                <input type="number" onChange={scoreChange} min={0} max={5} className="form-control" id="name" name="emScore"/> 
                <label htmlFor="emScore">How Strongly do you feel this 0-5</label>
                <button className="green_button" onClick={scoreOk}>Confirm</button>
             </div>
        </div>
    )

    let page =(
        <div>
            <div className="header">
                    <h1>Event Name</h1>
                    <button className="green_button" onClick={togglePopup}>Report Technical Issue</button>
            </div>
            <hr/>
            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>
            <hr/>
            <div className="row">
                <input type="text" className="form-control" id="name" name="Feedback" onChange={formHandler}/> 
                <label htmlFor="name">Provide Feedback</label>
            </div>
            <button className="green_button" onClick={sendFeedback}>Send</button>
        </div>
    )


    function toggleEmotionCb(id, value){
        setDisplayElement(1)
        setLastPressed(id)
        return true
    }
    
    //This is structured weirdly, but it's just so the pages are defined before we set the display element

    

    let f = page
    switch(displayElement){
        case 0:
            f=page
            break;
        case 1:
            f=emotionScore
            break;
        case 2:
            f=technicalIssue
            break;
        default:
            f=page
    }    

    
    return(
    <div>
        {f}
    </div>
    )
}