import "../styles.css"
import React, {useContext, useState, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import userFeedback from "../../api/userFeedback"

/**
 * Templates Need to look like this
 * template:{
 *      emotions:[]
 *      questions:[]
 * }
 */

function Question(props){
    if(!props.question){
        return null
    }
    const questionText = props.question.text
    const cb = props.question.callback

    function change(field){
        cb(field.target.value, props.id)
    }
    return(
        <div>
            <span><a>{questionText}</a></span> 
            <div className="row">
                    <input type="text" className="form-control" id="name" name="feedback" onChange={change}/>
                    <label htmlFor="name">Answer</label>
            </div>
        </div>
    )

}


export default function EosFeedback(){
    const location = useLocation()
    const template = location.state.template;
    const meetingdetails = location.state.meetingdetails
    console.log(template)
     
    const questions = template.questions
    const emotions = template.emotions

    const [questionValues, setQValues] = useState([])
    const [questionComponents, setQComponents] = useState([])

    useEffect(()=>{
        let tmpQComponents=[]
        let tmpQValues = []
        emotions.forEach(e=>{
            tmpEmValues.push(false)
        })
        questions.forEach(e=>{
            tmpQValues.push(false)
        })

        for(let i=0;i<questions.length;i++){
            let question ={
                text: questions[i],
                callback:onQuestionChange
            }
            tmpQComponents.push(<Question cb={onQuestionChange} question={question} key={i} id={i}/>)
        }

    },[])

    function onQuestionChange(value, id){
        console.log(questions[id])
        console.log(value+"\n")


    }

    for(let i=0;i<questions.length;i++){
        let question ={
            text: questions[i],
            callback:onQuestionChange
        }
        questionComponents.push(<Question question={question} key={i} id={i}/>)
    }

    function sendFeedback(){
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
            emotion: "Post",
            ftime:time
        }
    }
    

    //todo add meeting name
    return(
        <div>
        <div className="wrap">
            <h1> Meeting Name </h1> 
            <p>End-of-session feedback</p>
        </div>
        <hr/>
        <div className="wrap">
            <div className="row">
                {questionComponents}
            </div>

            <div>
                <button type="submit" className="green_button" onChange={sendFeedback}>Submit</button>
            </div>
        </div>
    </div>
    )
}