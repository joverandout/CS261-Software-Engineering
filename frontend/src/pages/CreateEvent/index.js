import "../styles.css"
import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';

export default function PublishEvent(){
    let location = useLocation()


    function formChange(formObj){
        console.log(formObj.target.value)
    }
    
    function showRecuranceDropdown(){
        console.log("pressed!")
    }

    function makeNewTemplate(){
    
    }

    function startEvent(){
        console.log("Starting!!")
    }

    function scheduleEvent(){
        console.log("scheduling!!")
    }

    let newCategoryField = (
        <div className="row">
            <input type="text" className="form-control" id="catInput" onChange={formChange}/>
            <label id="catInputLabel" htmlFor="name" >New Category Name</label>
        </div>  
    )

    let recurrance =(
        <select name="recurrenceFrequency" id="recurrenceFrequency" onChange={formChange}>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
        </select>
    )

    return (
        
        <div>
            <div className="header">
            <button className="white_button" id="back_button">Back</button>
            <h1>Create New Event</h1>

            </div>
            <div className="wrap">
                <div className="row">
                    <p style={style.genericText}> Event Name: </p>
                    <input type="text" className="form-control" id="name" onChange={formChange}/>    
                </div>

                <div>
                    <p style={style.genericText}> Select a Category: </p>
                    <select name="cat" id="cat" onChange={formChange}>
                        <option> --Select Category-- </option>
                        <option value="new"> Add New Category </option>
                    </select>
                </div>
                {/**{newCategoryField}*/}
                <div>
                    <p style={style.genericText}>Event Start Time:</p>
                    <input type="datetime-local" id="datetime" name="datetime" onChange={formChange}/>
                </div>

                <div className="oneLine">
                    <p style={style.genericText}> Event Duration (Hours): </p>
                    <input type="number" min={1} className="form-control" id="duration" onChange={formChange}/>
                    
                </div>


                <div className="oneline">
                    <p style={style.genericText}> Make Meeting Recurring: </p>
                    <input type="checkbox" id="recurringMeetingCheckbox" onClick={showRecuranceDropdown}/>
                    {/** recurrance */}
                </div>

                <div>
                    <p style={style.genericText}> Select an existing template:</p>
                    <select name="template" id="template">
                        <option> --Select Template-- </option> 
                        {/** get templates from user */}
                    </select>
                    <p style={style.genericText}>Or</p>
                    <input type="button" onClick="" value="Make a new Template" onClick={makeNewTemplate}/>
                </div>

                <button className="yellow_button" onClick={scheduleEvent}>Schedule Event</button>

                <button className="green_button" onClick={startEvent}>Start Event Now</button>


            </div>

            <hr/>
        </div>
    );
}

const style = {
    genericText:{fontSize: 20, fontWeight: "bold", textAlign: "left"}
}