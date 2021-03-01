import "../styles.css"
import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';

export default function PublishEvent(){
    let location = useLocation()
    let eventName = location.state.event.eventName
    console.log(location)

    //todo add qrcode
    //todo date checking
    //todo add back button functionality 
    return (
        
        <div>
            <button className="white_button" id="back_button" >Back</button>
            <div className="header">
                <h1>Publish Event</h1>
            </div>
            <hr/>
            <div className="wrap">

                    <br/>

                    <p>Do you want to start the following event?</p><br/>
                    <p style={{fontSize: "xx-large"}}>{eventName}</p> 
                    <br/><p>Scheduled for:</p><br/>
                    <a>///// Date if applicable, else just print 'Now' ////</a>


                    <div>
                        <button className="green_button">Start Event</button>
                    </div>
            </div>
        </div>
    );
}