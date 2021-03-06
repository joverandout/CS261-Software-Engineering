import "../styles.css"
import React, {useContext, useState, useCallback, useEffect} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import EmotionButton from "../../components/emotion_button"
import templateCreation from "../../api/templateCreation"
import userContext from "../../contexts/user-context";


export default function CreateTemplate(){
    let eList = [["Proud", "#F4b72f"],["Excited","#F4b72f"],["Interested", "#F4b72f"], ["Happy", "#F4b72f"], ["Joyful", "#F4b72f"], ["Optimistic", "#75C7E3"], ["Tired", "#75C7E3"], ["Calm", "#75C7E3"], ["Grateful", "#75C7E3"], ["Bored", "#75C7E3"], ["Sad", "#9B75E3"], ["Insecure", "#9B75E3"], ["Depressed", "#9B75E3"], ["Anxious", "#9B75E3"], ["Afraid", "#9B75E3"], ["Annoyed", "#F07A7A"], ["Angry", "#F07A7A"], ["Overwhelmed", "#F07A7A"], ["Stressed", "#F07A7A"], ["Frustrated", "#F07A7A"]];

    const [customEmName, setCustomName] = useState("");
    const [buttonValues, setButtonValues] = useState([])
    const [emotionButtons, setEmButtons] = useState([])
    const [questions, setQuestions] = useState([])
    const [questionPs, setQPs] = useState([])
    const [newQ, setNewQ] = useState("")
    const [form, setForm] = useState({})

    const [id, setID] = useState(-1)
    const [val, setVal] = useState(false)

    const contextUser = useContext(userContext)
    const user = contextUser.user
    const history = useHistory()
    useEffect(()=>{
        console.log("!!")
        let tmpValues = []
        let tmpButtons = []
        eList.forEach((em, i)=>{
            let name = em[0]
            tmpValues.push(false)
            tmpButtons.push(<EmotionButton name={name} value={false} toggleEmotionCb={toggleEmotionCb} key={i} id={i}/>)
            //console.log(i)
        })
    
        setEmButtons(tmpButtons)
        setButtonValues(tmpValues)
    },[])

    useEffect(()=>{
        let tmpEmValues = buttonValues
        console.log(id, val)
        tmpEmValues[id] = val
        setButtonValues([...tmpEmValues])
    }, [id, val])
    
    function toggleEmotionCb(id, value){
        
        setVal(value)
        setID(id)
        return true
    }

    function customEmHandler(inObj){
        setCustomName(inObj.target.value)
    }

    function addButton(){
        let tmpEmButton = emotionButtons
        let tmpEmValues = buttonValues
        let i = emotionButtons.length
        tmpEmButton.push(<EmotionButton value={false} toggleEmotionCb={toggleEmotionCb} name={customEmName} key={i} id={i}/>)
        tmpEmValues.push(false)

        setButtonValues([...tmpEmValues])
        setEmButtons([...tmpEmButton])
    }

    function newQuestionHandler(formObj){
        setNewQ(formObj.target.value)
    }

    function addQuestion(){
        let q = newQ
        
        if(q.charAt(q.length-1) !="?"){
            q+="?"
        }
        
        setQuestions([...questions, q])
        setQPs([...questionPs, (<p key={questionPs.length}>{q}</p>)])
    }

    function complete(){
        //? seperated sstring
        let finalQuestions = questions.join("")
        let emotions = []
        buttonValues.forEach((bool, i)=>{
            if(bool){
                console.log(emotionButtons[i].props.name)
                emotions.push(emotionButtons[i].props.name)
            }
        })
        let tmpForm = form
        tmpForm.emotionsselected = emotions.join()
        tmpForm.question = finalQuestions
        tmpForm.hostid = user.hostid.toString()
        setForm(tmpForm)
        console.log(tmpForm)
        templateCreation(tmpForm).then(res=>{
            console.log("Yay we made it")
            history.goBack()
        }).catch(err=>{
            console.log(err.message)
        })
    }

    function formChange(formObj){
        let name = formObj.target.name
        let value = formObj.target.value
        let tmpForm = form
        tmpForm[name] = value 
        if(!tmpForm.templatename){
            return
        }
    }

    function back(){
        history.goBack()
    }   
    console.log("FF",buttonValues, emotionButtons.length)
    //console.log(buttonValues.length)
    return(
        <div>
            <button className="white_button" id="back_button" onClick={back}>Back</button>
            <div className="header">
                <h1>New Template</h1>
            </div>
            <hr/>

            <div className="wrap">

                <div className="row">
                    <input name={"templatename"} type="text" className="form-control" id="name" onChange={formChange}/>
                    <label htmlFor="name">Template Name</label>
                </div>
            </div>

            <p className="largerFont">Select up to 8 emotions for attendees to choose from:</p>

            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>

            <div>
                <h2>Questions</h2>
                {questionPs}
            </div>

            <div className="wrap">
                <div className="oneline">
                    <p>Add custom emotion: </p>
                    <input type="text" className="form-control" id="name" onChange={customEmHandler}/>
                    <button type="button" className="yellow_button" onClick={addButton}>Add</button>
                </div>

                <div className="oneline">
                    <p>Add new question: </p>
                    <input type="text" className="form-control" id="name" onChange={newQuestionHandler}/>
                    <button type="button" className="yellow_button" onClick={addQuestion}>Add</button>
                </div>
                
            </div>      
            <button type="submit" className="green_button" id="next_button" onClick={complete}>Next</button>


        </div>
    );
}

