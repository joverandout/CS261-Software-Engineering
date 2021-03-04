import "../styles.css"
import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import EmotionButton from "../../components/emotion_button"

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
    /* const template = location.state.template;
     */
    const template = {
        emotions: ["Sad", "Happy", "Numb"],
        questions: ["What did you think of xyz", "Was everyting clear and consice", "Questions?"]
    }
    const questions = template.questions
    const emotions = template.emotions

    let tmpEmValues = []
    let tmpQValues = []
    let emotionButtons = []
    let questionComponents=[]
    emotions.forEach(e=>{
        tmpEmValues.push(false)
    })
    questions.forEach(e=>{
        tmpQValues.push(false)
    })
    const [emotionValues, setEmValues] = useState(tmpEmValues)
    const [questionValues, setQValues] = useState(tmpQValues)

    function toggleEmotionCb(id, value){
        let tmpEmValues = emotionValues;
        let val = emotionValues[id]
        tmpEmValues[id] = (val?false:true)
        setEmValues(tmpEmValues)
        return true
    }

    function onQuestionChange(value, id){
        console.log(questions[id])
        console.log(value+"\n")
    }

    for(let i=0;i<emotions.length;i++){
        let emotion={
            name: emotions[i],
            color: "#F4b72f"
        }
        emotionButtons.push(<EmotionButton toggleEmotionCb={toggleEmotionCb} emotion={emotion} key={i} id={i}/>)
    }

    for(let i=0;i<questions.length;i++){
        let question ={
            text: questions[i],
            callback:onQuestionChange
        }
        questionComponents.push(<Question question={question} key={i} id={i}/>)
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

            <br/>
            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>

            <div>
                <button type="submit" className="green_button">Submit</button>
            </div>
        </div>
    </div>
    )
}