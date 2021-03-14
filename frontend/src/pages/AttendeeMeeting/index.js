import "../styles.css"
import "./popup_styles.css"

import React, {useContext, useState, useCallback, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import x2 from "./x2.png";
import EmotionButton from "../../components/emotion_button"
import userFeedback from "../../api/userFeedback"

import {io} from "socket.io-client"

export default function AttendeeMeeting(){
    const location = useLocation();
    const meetingdetails = location.state.meetingdetails
    const template = meetingdetails.template
    const history = useHistory()
    
    const [emotionButtons, setEmotionButtons] = useState([])
    const [emotionValues, setEmValues] = useState([])
    const [displayElement, setDisplayElement] = useState(0)
    const [lastPressed, setLastPressed] = useState(null)
    const [score, setScore] = useState(0)
    const [popup, setPopup] = useState(false)
    const [feedback, setFeedback] = useState("")
    const [tFeedback, setTFeedback] = useState("")

    useEffect(()=>{
        //create all the emotion buttons from the template information received from the server
        let tmpEmValues = []
        let tmpEmButtons = []
        meetingdetails.template.emotions.forEach((emotion,i)=>{
            tmpEmValues.push(0)
            tmpEmButtons.push(<EmotionButton name={emotion} toggleEmotionCb={toggleEmotionCb} value={false} id={i} key={i}/>)
        })
        setEmotionButtons(tmpEmButtons)
        setEmValues(tmpEmValues)
        //Open the socket connection to the server
        const socket = io("http://127.0.0.1:5000", {
            auth:{
            token:"id01043"
            }
        })
        socket.on("endmeeting", meetingOver)
        return ()=>{
            socket.close()
            console.log("closing")
        }
    },[])

    //When the emotion values have changed, ensure that all the buttons reflect the proper value
    useEffect(()=>{
        let tmpEmButtons=[]
        
        emotionValues.forEach((val,i)=>{
            let value = (val>0)?true:false
            
            let name = meetingdetails.template.emotions[i]
            tmpEmButtons.push(<EmotionButton name={name} toggleEmotionCb={toggleEmotionCb} value={value} id={i} key={i}/>)
        })
        
        setEmotionButtons([...tmpEmButtons])
        setDisplayElement(0)
        
    }, [emotionValues])

    //When we get the signal for the meeting tp be over, navigate to the End of Session feedback page
    function meetingOver(data){
        if(data=="ok"){
            history.push({
                pathname: "/EosFeedback",
                state:{
                    template:template,
                    meetingdetails:meetingdetails
                }
            })
        }
    }
    
    //Display either the technical feedback prompt or the regular feedback prompt
    function togglePopup(){
        let tmpPopup = popup?false:true 

        if(tmpPopup){
            setDisplayElement(2)
        }else{
            setDisplayElement(0)
        }
        setPopup(tmpPopup)
    }

    //Set the score value based on the button pressed. The value is the same as the name attribute of the button
    function scoreOk(bObj){
        let score = bObj.target.name
        console.log(score)
        let tmpEmValues = emotionValues
        tmpEmValues[lastPressed] = parseInt(score)
        setEmValues([...tmpEmValues])
        
        setScore(0)
    }

    //Enure the feedback hook reflects the information being input
    function formHandler(formObj){
        setFeedback(formObj.target.value)
    }

    //When a technical issue button is pressed, send the feedback to the server immediately
    function issueButton(buttonObj){
        let name = buttonObj.target.name
        let now = new Date()
        let h = now.getHours().toString()
        let m = now.getMinutes().toString()
        let s = now.getSeconds().toString()
        let time = h+":"+m+":"+s
        let data={
            generaltext:name,
            meetingid: meetingdetails.meetingid.toString(),
            companyid: meetingdetails.companyid.toString(),
            rating: "null",
            emotion: "Technical",
            ftime:time
        }
        userFeedback(data).then(res=>{
            //refresh all the values
            console.log("Feedback successfully sent")
        }).catch(err=>{
            console.log(err.message)
        })
        setDisplayElement(0)
    }   
    //Send technical text feedback when the button is pressed
    function sendTechnical(){
        let now = new Date()
        let h = now.getHours().toString()
        let m = now.getMinutes().toString()
        let s = now.getSeconds().toString()
        let time = h+":"+m+":"+s
        if(tFeedback == ""){
            return
            //todo nothing entered error
        }
        let data={
            generaltext:tFeedback,
            meetingid: meetingdetails.meetingid.toString(),
            companyid: meetingdetails.companyid.toString(),
            rating: "null",
            emotion: "Technical",
            ftime:time
        }
        setDisplayElement(0) //make sure we go back to displaying the origional screen
        userFeedback(data).then(res=>{
            //todo refresh all the values
            console.log("Feedback successfully sent")
        }).catch(err=>{
            console.log(err.message)
        })
    }   

    //Send emotion or regular text feedback
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
        let sum = scores.reduce((a, b) => parseInt(a) + parseInt(b), 0)
        //if nothing is entered dont send the feedback
        if(data.generaltext=="" && sum==0){
            return
        }

        userFeedback(data).then(res=>{
            //refresh all the values
            console.log("Feedback successfully sent")
            setFeedback("")
            let tmpEmValues = []
            emotionValues.forEach(e=>{
                tmpEmValues.push(0)
            })
            setDisplayElement(1)
            setEmValues([...tmpEmValues])
            
        }).catch(err=>{
            console.log(err.message)
        })
    }

    function toggleEmotionCb(id, value){
        setDisplayElement(1)
        setLastPressed(id)
        return true
    }
    
    let technicalIssue = (
        <div  id="reportIssue">
        <div className="form-container report-container">
        <button onClick = {togglePopup} className="exit"><img src={x2} /> </button>
        <h1>Report an issue</h1>
        <button name="The speaker is too quiet" className="btn report" onClick={issueButton}>The speaker is too quiet</button>
        <button name="The speaker is muted" className="btn report" onClick={issueButton}>The speaker is on mute</button>
        <button name="Meeting Content is missing" className="btn report" onClick={issueButton}>The content is missing</button>
        <br></br>
        <br></br>
        <div className="row">
            <input type="text" className="form-control" id="name" name="Issue" onChange={(input)=>{setTFeedback(input.target.value)}}/> 
            <label htmlFor="name">Report other issue</label>
            <button className="btn report" onClick={sendTechnical}>Send</button>
        </div>
        </div>
    </div>
    )

    
    
    let emotionScore=(
        <div>
            <div className="row">
                
                <label htmlFor="emScore">How strongly do you feel this?</label>
                <br></br><br></br><br></br><br></br><br></br>
                <div>
                    <button className="green_button" name={1} onClick={scoreOk}>1 - Slightly</button>
                    <button className="green_button" name={2} onClick={scoreOk}>2 - A little</button>
                    <button className="green_button" name={3} onClick={scoreOk}>3 - Fairly</button>
                    <button className="green_button" name={4} onClick={scoreOk}>4 - Moderately</button>
                    <button className="green_button" name={5} onClick={scoreOk}>5 - Extremely</button>
                    <button className="red_button" name={0} onClick={scoreOk}>Back</button>
                </div>
                
             </div>
        </div>
    )

    let page =(
        <div>
            <div className="header">
                    <h1>{meetingdetails.meetingname}</h1> 
                    <button className="red_button" onClick={togglePopup}>Report Technical Issue</button>
            </div>
            <br></br>
            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>
            <br></br>
            <div className="wrap">
            <div className="row">
                <input value={feedback} type="text" className="form-control" id="name" name="Feedback" onChange={formHandler}/> 
                <label htmlFor="name">Provide Feedback</label>
            </div>
            </div>
            <button className="green_button" onClick={sendFeedback} style={{marginTop: 50, marginBottom: 60}}>Send</button>
        </div>
    )


    let f = null
    switch(displayElement){ //ensure the correct elements are being displayed
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