import "../styles.css"
import React, {useContext, useState, useCallback, useEffect, useRef} from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import EmotionButton from "../../components/emotion_button"
import templateCreation from "../../api/templateCreation"
import userContext from "../../contexts/user-context";

export default function CreateTemplate(){

    const [customEmName, setCustomName] = useState("");
    const [buttonValues, setButtonValues] = useState([])
    const [emotionButtons, setEmButtons] = useState([])
    const [eList, setEList] = useState([["Proud", "#F4b72f"],["Excited","#F4b72f"],["Interested", "#F4b72f"], ["Happy", "#F4b72f"], ["Joyful", "#F4b72f"], ["Optimistic", "#75C7E3"], ["Tired", "#75C7E3"], ["Calm", "#75C7E3"], ["Grateful", "#75C7E3"], ["Bored", "#75C7E3"], ["Sad", "#9B75E3"], ["Insecure", "#9B75E3"], ["Depressed", "#9B75E3"], ["Anxious", "#9B75E3"], ["Afraid", "#9B75E3"], ["Annoyed", "#F07A7A"], ["Angry", "#F07A7A"], ["Overwhelmed", "#F07A7A"], ["Stressed", "#F07A7A"], ["Frustrated", "#F07A7A"]])


    const [newQ, setNewQ] = useState("")
    const [questions, setQuestions] = useState([])
    const [questionBs, setQBs] = useState([])
    const [delQ, setDelQ] = useState([""])
    const [count, setCount] = useState(-1) //redunant hook
    const [qCount, setQCount] = useState(0)
    const c = useRef(0)


    const [form, setForm] = useState({})

    //Dirty fix, should use a reference 
    const [id, setID] = useState(-1)
    const [val, setVal] = useState(true)

    const contextUser = useContext(userContext)
    const user = contextUser.user
    const history = useHistory()

    //create the initial buttons on loadin
    useEffect(()=>{
        
        let tmpValues = []
        let tmpButtons = []
        eList.forEach((em, i)=>{
            let name = em[0]
            tmpValues.push(false)
            tmpButtons.push(<EmotionButton name={name} value={false} toggleEmotionCb={toggleEmotionCb} key={i} id={i}/>)
        })
    
        setEmButtons(tmpButtons)
        setButtonValues(tmpValues)
    },[])

    //dirty fix to problem, should use a reference
    useEffect(()=>{
        
        let tmpEmValues = buttonValues
        let increment = val?1:-1
    
        c.current = count+increment
        tmpEmValues[id] = val
        setCount(count+increment)
        setButtonValues([...tmpEmValues])
    }, [id, val])
    
    function toggleEmotionCb(id, value){
        console.log("Callback",c,value)
        if(c.current+1>8 && value == true){
            return false // do not allow buttons to toggle true if 8 already exist
        }
        setVal(value)
        setID(id)
        return true
    }

    function customEmHandler(inObj){
        setCustomName(inObj.target.value)
    }

    //update the questions if one was deleted
    useEffect(()=>{
        setQuestions(questions.filter(q=>q!=delQ))
        setQBs(questionBs.filter(qb=>qb.props.name!=delQ))
    },[delQ])


    function addButton(){
        
        if(customEmName == ""){
            return
            // Add error message?
        }

        //if the name already exists, do not leat a new button to be created
        for(let i=0;i<eList.length;i++){
            if(eList[i][0]==customEmName){
                return
                //add error message
            }
        }

        let tmpEmButton = emotionButtons
        let tmpEmValues = buttonValues
        let i = emotionButtons.length
        tmpEmButton.push(<EmotionButton value={false} toggleEmotionCb={toggleEmotionCb} name={customEmName} key={i} id={i}/>)
        tmpEmValues.push(false)

        setButtonValues([...tmpEmValues])
        setEmButtons([...tmpEmButton])
        setEList([...eList, [customEmName,""]])
    }

    function newQuestionHandler(formObj){
        setNewQ(formObj.target.value)
    }

    function addQuestion(){
        let q = newQ
        
        if(q.charAt(q.length-1) !="?"){ // questions must end with ?
            q+="?"
        }
        
        if(q==""||questions.includes(q)){ //no repeat questions
            return 
            //Add some kind of error message
        }

        if(questions.length == 3){
            return 
            //another error message
        }
        
        let newQB = (<button className="question_box" key={qCount} name={q} onClick={deleteQuestion}>{q}</button>)
        setQCount(qCount+1)
        setQuestions(questions.concat(q))
        setQBs(questionBs.concat(newQB))
        setNewQ("")
       
    }

    function deleteQuestion(bqObj){
        setDelQ(bqObj.target.name)
    }

    //send all the collected information back to the server
    function complete(){
        //? seperated sstring
        let finalQuestions = questions.join("")
        let emotions = []
        buttonValues.forEach((bool, i)=>{
            if(bool){
               
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
            history.goBack()
        }).catch(err=>{
            console.log(err.message)
        })
    }

    //change the form details when one of the inputs change
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

    return(
        <div>
            <button className="white_button" id="back_button" onClick={back}>Back</button>
            <div className="header">
                <h1>New Template</h1>
            </div>
            <hr/>

            <br></br>
            <div className="wrap">

                <div className="row">
                    <input name={"templatename"} type="text" className="form-control" id="name" onChange={formChange}/>
                    <label htmlFor="name">Template Name</label>
                </div>
            </div>

            <br></br>
            <br></br>
            <h2>Emotions</h2>
            <p className="largerFont">Ask attendees how they are feeling.</p>
            <p className="largerFont"> Select up to 8 emotions for attendees to choose from:</p>

            <div className="btn-group" id="buttons" style={{marginBottom: 60}}>
                {emotionButtons}
            </div>

            <div className="wrap">
                <div className="row">
                    <input type="text" className="form-control" id="name" onChange={customEmHandler}/>
                    <label htmlFor="name">Custom Emotion</label>
                    <button type="button" className="yellow_button" onClick={addButton}>Add</button>
                </div>
            </div>


            <div>
                <br></br>
                <br></br>
                <h2>End of Session Questions</h2>
                <p className="largerFont">Ask attendees questions after the session</p>
                {questionBs}
            </div>

            <div className="wrap">
                <div className="row">
                    <input type="text" className="form-control" id="name" onChange={newQuestionHandler} value={newQ}/>
                    <button type="button" className="yellow_button" onClick={addQuestion}>Add</button>
                </div>
            </div>

            <button type="submit" className="green_button" id="next_button" onClick={complete}>Next</button>


        </div>
    );
}

