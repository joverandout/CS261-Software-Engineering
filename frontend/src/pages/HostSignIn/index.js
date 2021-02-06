
import React, {useState} from 'react';
import ReactDOM from 'react-dom';



export default function HostSignIn(){
  const [signedIn, setSignedIn] = useState(false);

  function signin(){
    console.log("Pressed!")
    setSignedIn(signedIn != true);
  }

  let signedInIndicator = (<h2>Signed in: {signedIn.toString()}</h2>);


  const page = (
    <div>
      <h1>Host Sign In Page</h1>
      {signedInIndicator}
      <button onClick={signin}>
        Sign In
      </button>
    </div>
  )
  return page
}