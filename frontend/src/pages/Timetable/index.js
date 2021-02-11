
import React, { useState } from 'react';
import {io} from "socket.io-client"

const socket = io("http://127.0.0.1:5000", {
  auth:{
    token:"id01043"
  }
})

socket.on("connect", ()=>{
  console.log("Connection Made!")
  console.log(socket.id)
})

socket.on("disconnect", () => {
  console.log("Disconnecting")
  console.log(socket.id); // undefined
});

export default function HostSignIn(){
  const [smessage, setSmessage] = useState("...")

  function socketMessage(){
    socket.emit("hello", "hello server :)")
  }

  socket.on("femessage", data=>{
    setSmessage(data.message)
  })

  let message = (<h2>{smessage}</h2>)

  return(
    <div>
    <h1>Hello, world! - Timetable</h1>
    {message}
    <button onClick={socketMessage}>
      text
    </button>
    </div>
  );
}