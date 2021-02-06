import React from 'react'; 
import { Route, Redirect } from 'react-router-dom';  
export default function RouteWrapper({   
  component: Component,   
  isPrivate,   
  ...rest 
}) {   
  const signed = false; 
  // set to true, but in the future we will need some kind of state-remembering-system to tell if we actually have signed in
  
  /**    
  * Redirect user to SignIn page if they try to access a private      route
  * without authentication.    
  */   
  if (isPrivate && !signed) {     
    return <Redirect to="/" />;   
  }      
  /**    
  * Redirect user to Main page if they try to access a non private route    
  * (SignIn or SignUp) after being authenticated.    
  */   
  if (!isPrivate && signed) {     
    return <Redirect to="/Timetable" />;   
  }    
  
  /**    
  * If not included on both previous cases, redirect user to the desired route.    
  */   
  return <Route {...rest} component={Component} />; 

  /**
   * ... is a weird operator i still dont fully understand. afaik ...rest is just any random 
   * extra arguments we decide to pass, so if neiter of the if statements pass, just go to the page 
   * they asked for and send all the extra info along with it 
   * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
   * 
   * 
   * Also havent done prop type validation as that article suggests as we may aswell use typescript if thats what we're after
   */
}