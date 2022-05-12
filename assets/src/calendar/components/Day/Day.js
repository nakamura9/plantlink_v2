/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {useState, useEffect} from 'react';
import Event from '../Event';
import Context from '../../container/provider'
import {intervals} from '../Week/WeekView'
import styles from './Day.css'


const day = (props) => {
    //calculate the dimensions of the day
    const [eventList, setEventList] = useState([])
    const wrapperClass = props.view == "week" 
        ? styles.weekViewDayWrapper 
        : styles.dayWrapper

    const dimensionStyle = {
        width: `${props.width}px`,//here
        height: `${props.height}px`
    }

    const clickDay = () => {
        if(!props.showDay) return
        props.setDate({
            year: props.data.date.getFullYear(),
            month:props.data.date.getMonth(),
            day: props.data.day,
            view: 'day'
        })
    }

    useEffect(() => {
        const list = [];
        for(let evt of props.events){
            if(props.data.current && 
                    new Date(evt.date).getDate() == props.data.date.getDate()){
                list.push(evt)
            }
        }
        setEventList(list)
    }, [props.events])

    return(
        <Context.Consumer>{
            context=>(
                <div
                className={wrapperClass}
                style={{width: `${props.width}px`,}}
                >
                    <div>
                        {props.view == 'week' 
                            ? <span className={styles.dayLabel}>
                                <span onClick={clickDay}>{props.data.day}</span>
                            </span>
                            : <h1
                                className={styles.weekViewDayHeader}
                                style={{backgroundColor: context.accent}}
                            >
                                {props.data.date}
                            </h1>
                        }
                    </div>
                    <div className="position-relative"
                    style={dimensionStyle}>
                    { eventList.map((event, i) =>(
                        <Event 
                            width={props.width}
                            key={i} 
                            data={event}
                            view={props.view}/>
                    ))}
                    </div>
                </div>)
        }</Context.Consumer>
    )
}


export default day;