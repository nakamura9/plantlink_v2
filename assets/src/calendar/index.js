import React from 'react';
import CalendarApp from './container/Root';
import ReactDOM from 'react-dom/client'

const root = document.getElementById('root')

const renderer = ReactDOM.createRoot(root)

renderer.render(
    <CalendarApp 
        showMonth
        showWeek
        showDay
        primaryColor="steelblue"
        accentColor="#007bff"
        offsetTop={10}
        monthHook={() => console.log("Hook!")}
        weekHook={() => console.log("Hook!")}
        dayHook={() => console.log("Hook!")}
    />
)