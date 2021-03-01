import "../styles.css"
import React, {useContext, useState, useCallback, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import EmotionButton from "../../components/emotion_button"


export default function CreateTemplate(){
    let eList = [["Proud", "#F4b72f"],["Excited","#F4b72f"],["Interested", "#F4b72f"], ["Happy", "#F4b72f"], ["Joyful", "#F4b72f"], ["Optimistic", "#75C7E3"], ["Tired", "#75C7E3"], ["Calm", "#75C7E3"], ["Grateful", "#75C7E3"], ["Bored", "#75C7E3"], ["Sad", "#9B75E3"], ["Insecure", "#9B75E3"], ["Depressed", "#9B75E3"], ["Anxious", "#9B75E3"], ["Afraid", "#9B75E3"], ["Annoyed", "#F07A7A"], ["Angry", "#F07A7A"], ["Overwhelmed", "#F07A7A"], ["Stressed", "#F07A7A"], ["Frustrated", "#F07A7A"]];
    const [emotions, setEmotions] = useState(eList)
    const [emotionButtons, setEmButtons] = useState([])
    const [emotionValues, setEmValues] = useState([])

    const [customEmotion,setCustomEm] = useState("")
    //todo finish create template functions
    function customEmHandler(inObj){
        setCustomEm(inObj.target.value)    
    }

    function formChange(formObj){
        console.log(formObj.target.value)
    }
    
    function complete(){

    }

    function addButton(){
        //todo clear the entry field when this is pressed
        if(customEmotion == ""){
            return
        }
        //todo change this color
        let tmpEmotions = emotions;
        tmpEmotions.push([customEmotion, "#F4b72f"])
        setEmotions([...tmpEmotions])
        setCustomEm("") //this isnt good enough

    }
    //todo, make this a object with the emotions as keys inst
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

    function refreshButtons(){
        let diff = emotions.length-emotionButtons.length;
        let tmpEmButtons = emotionButtons
        let tmpEmValues = emotionValues
        let offset = emotionButtons.length

        for (let i=offset; i<diff+offset; i++) {
            
            let emotion={
                name: emotions[i][0],
                color: emotions[i][1]
            }
            tmpEmButtons.push(<EmotionButton toggleEmotionCb={toggleEmotionCb} emotion={emotion} key={i+offset} id={i+offset}/>)
            tmpEmValues.push(false)
        }
        setEmButtons([...tmpEmButtons])
        setEmValues(tmpEmValues)
    }

    useEffect(()=>{
        refreshButtons()
        console.log("refresh!!!")
    },[emotions])

    if(emotionButtons.length == 0){
        refreshButtons()
    }
    
    return(
        <div>
            <button className="white_button" id="back_button">Back</button>
            <div className="header">
                <h1>New Template</h1>
            </div>
            <hr/>

            <div className="wrap">

                <div className="row">
                    <input type="text" className="form-control" id="name" onChange={formChange}/>
                    <label htmlFor="name">Template Name</label>
                </div>
            </div>

            <p className="largerFont">Select up to 8 emotions for attendees to choose from:</p>

            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>

            <div className="wrap">
                 <div className="oneline">
                    <p>Add custom emotion: </p>
                    <input type="text" className="form-control" id="name" onChange={customEmHandler}/>
                    <button type="button" className="yellow_button" onClick={addButton}>Add</button>
                </div>
                
            </div>      
            <button type="submit" className="green_button" id="next_button" onClick={complete}>Next</button>


        </div>
    );
}

