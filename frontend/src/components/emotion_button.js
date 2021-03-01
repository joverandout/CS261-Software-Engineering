import "../styles.css"
import "../template_styles.css"
import React, { useState} from 'react';

export default function EmotionButton(props){
    const [value, setValue] = useState(false)
    const [btnStyle, setStyle] = useState({backgroundColor:""})

    if(!props.emotion){
        return null
    }


    let toggleEmotionCb = props.toggleEmotionCb
    
    function toggle(){
        let newVal = (value ? false:true);
        
        if(!toggleEmotionCb(props.id, newVal)){
            return
        }
        setValue(newVal)
        if(newVal){
            setStyle({backgroundColor: props.emotion.color})
        }else{
            setStyle({backgroundColor: ""})
        }
    }

    return(
        <button style={btnStyle} onClick={toggle}>{props.emotion.name}</button>
    )
}