import "../styles.css"
//import "../template_styles.css"
import React, { useState, useEffect} from 'react';
const eList = [["Proud", "#F4b72f"],["Excited","#F4b72f"],["Interested", "#F4b72f"], ["Happy", "#F4b72f"], ["Joyful", "#F4b72f"], ["Optimistic", "#75C7E3"], ["Tired", "#75C7E3"], ["Calm", "#75C7E3"], ["Grateful", "#75C7E3"], ["Bored", "#75C7E3"], ["Sad", "#9B75E3"], ["Insecure", "#9B75E3"], ["Depressed", "#9B75E3"], ["Anxious", "#9B75E3"], ["Afraid", "#9B75E3"], ["Annoyed", "#F07A7A"], ["Angry", "#F07A7A"], ["Overwhelmed", "#F07A7A"], ["Stressed", "#F07A7A"], ["Frustrated", "#F07A7A"]];

/**
 * 
 * @param {name: , value: , id: } props 
 * @returns A coloured button displaying the name of an emotion that changes colour when clicked
 */
export default function EmotionButton(props){

    const [value, setValue] = useState(props.value)
    const [baseColour, setBaseColour] = useState("")
    const [btnStyle, setStyle] = useState({backgroundColor:""})
    
    useEffect(()=>{
        let set = false
        let colour = ""
        //Set the colour for the button, use predefined colours if they exist
        eList.forEach(e=>{
            if(props.name == e[0]){
                setBaseColour(e[1])
                set = true
                colour = e[1]
            }
        })

        //if no predefined colour exists, set it to a default green
        if(!set){
            setBaseColour("#B9DFA0")
            colour = "#B9DFA0"
        }

        if(props.value == true){
            
            setStyle({backgroundColor:colour})
        }else{
            setStyle({backgroundColor:""})
        }
    },[])

    let toggleEmotionCb = props.toggleEmotionCb
    //change colour when the toggle button callback returns true, usually if less than 8 have been pressed
    function toggle(){
        let newVal = (value ? false:true);
        
        if(!toggleEmotionCb(props.id, newVal)){
            return
        }
        setValue(newVal)
        if(newVal){
            setStyle({backgroundColor: baseColour})
        }else{
            setStyle({backgroundColor: ""})
        }
    }

    return(
        <button className="emotion_button" style={btnStyle} onClick={toggle}>{props.name}</button>
    )
}