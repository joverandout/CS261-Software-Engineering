import "../styles.css"
import React, {useContext, useState, useMemo, useEffect} from 'react';
import { Chart } from "react-charts"


const socket = io("http://127.0.0.1:5000/");



export default function HostMeeting(){
    const data = useMemo(
        () => [
          {
            label: 'Series 1',
            data: [[0, 1], [1, 2], [2, 4], [3, 2], [4, 7]]
          },
          {
            label: 'Series 2',
            data: [[0, 3], [1, 1], [2, 5], [3, 6], [4, 4]]
          }
        ],
        []
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
            width: '400px',
            height: '300px'
          }}
        >
          <Chart data={data} axes={axes} />
        </div>
      )

    return(
        <div>
            {lineChart}
        </div>
    )
}

