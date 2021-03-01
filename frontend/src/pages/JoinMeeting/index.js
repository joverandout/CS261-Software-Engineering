import "../styles.css"
import React, {useContext, useState, useCallback} from 'react';
import { useLocation, useHistory } from 'react-router-dom';

export default function JoinMeeting(){

    return(
        <div className="wrap">
        <h1>Find a Meeting</h1>
            <div className="row">
                <input type="text" className="form-control" id="name" name="code" required/> 
                <label htmlFor="name">Meeting Code</label>
            </div>

            <div className="row">
                <input type="text" className="form-control" id="name" name="username" required/> 
                <label htmlFor="name">CompanyID</label>
            </div>

            <div className="row">
                <input type="text" className="form-control" id="name" name="username" required/> 
                <label htmlFor="name">Name</label>
            </div>
            
            <span><a id="AnonymousMessage">Remain Anonymous</a></span>
            <input type="checkbox" id="Anonymous" name="Anonymous" value="Anonymous"/>

            
            
            <div>
                <button type="submit" className="green_button">Join</button>
            </div>
            

    </div>
    )
}