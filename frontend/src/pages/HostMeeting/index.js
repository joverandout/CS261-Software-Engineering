import "../styles.css"
import React, {useReducer, useState, useMemo, useEffect} from 'react';
import { Chart } from "react-charts"
import {io} from "socket.io-client"

function reducer(state, action){
    switch(action.type){
        case "newSemantic":
            let currentSum = state.semanticData.sum
            let currentCount = state.semanticData.count
            let actionVal = action.semanticValue

           let newCount = currentCount+1
           let newSum = currentSum+actionVal
           let ave = newSum/newCount
           let plot = [...state.semanticData.plot, [Date.parse(Date()), ave]]
           console.log(plot)
           
           return {
               semanticData:{
                   sum:newSum,
                   count:newCount,
                   plot:plot
               }
           }
    }
}

export default function HostMeeting(){
    
    const initialState ={
        semanticData: {
            sum:0,
            count:0,
            plot:[[Date.parse(Date()), 0]]
        }
    }
    const [state, dispatch] = useReducer(reducer, initialState)

    useEffect(()=>{
      const socket = io("http://127.0.0.1:5000", {
        auth:{
          token:"id01043"
        }
      })
      socket.on("feedback", newFeedback)
    },[])
    
    function newFeedback(data){
       dispatch({
           type:"newSemantic",
           semanticValue:data.value
       })
    }
    
    const data = useMemo(
        () => [
          {
            label: 'Series 1',
            data: state.semanticData.plot//[[0,0],[1,1],[2,1],[3,-1]]
          }
        ]
      )
     
      const axes = useMemo(
        () => [
          { primary: true, type: 'utc', position: 'bottom' },
          { type: 'linear', position: 'left' }
        ],
        []
      )
     
      const lineChart = (
        // A react-chart hyper-responsively and continuously fills the available
        // space of its parent element automatically
        <div
          style={{
            width: '900px',
            height: '700px'
          }}
        >
          <Chart data={data} axes={axes} />
        </div>
      )

    return(
        <div>
            <p>{state.semanticData.count}</p>
            <hr/>
            {lineChart}
        </div>
    )
}

