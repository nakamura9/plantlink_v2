/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React from 'react';
import styles from './event.css';
import Context from '../container/provider'
import Radium from 'radium'


const Event = (props) =>{
    let startY = 90;
    let height = 44;
    
    if(props.view === "month"){
        startY = 0 + (props.position * 35);
        height = 32;
    }else{
        if(props.data.start){
            const start = parseInt(props.data.start.split(":")[0]);
            const end = parseInt(props.data.end.split(":")[0]);
            const yOffset = props.view == 'day' ? 108 : 18
            startY = yOffset + (start * 25);
            // for errors in recording the event times
            if(end > start){
                height = (end - start) * 25;
            }
        } else {
            startY = 90 + (props.position * 50);
        }
    }
    

    const startX = props.offset ? props.offset: 0;
    const linkStyle = {
        zIndex: props.index,
        left: props.view === "day" ? "60px" : "0px",
        top: `${startY}px`,
        width: props.view === "day" 
                ? "250px" : props.view === "week" ?
                 `${props.width}px` : `100%` ,
        
    }
    const divStyle = {
        height: `${height}px`,
        backgroundColor:props.context.primary,
        ':hover': {
            color: props.context.primary,
            backgroundColor: 'white',
            border: `1px solid ${props.context.primary}`,
            height: 'fit-content',
            transform: 'scale(1.125)',
            
        }
    }
    
    return( 
        <a
            className={styles.event}
            style={linkStyle} 
            href={props.data.id}>
            <div style={divStyle} className={styles.eventBox}>
                <div>
                    <span>{props.data.title}</span>
                </div>
                {props.description 
                    ? <div><p>{props.description}</p></div>
                    : null}
            </div>
        </a>
    );
}

const eventHOC = (props) => (
    <Context.Consumer>{context => (
        <Event {...props} context={context}/>
    )}</Context.Consumer>
)

export default Radium(eventHOC);