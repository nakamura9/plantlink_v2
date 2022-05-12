/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {useState, useEffect} from 'react';
import Event from '../Event';
import styles from './Day.css';
import HoverableEventList from './event_list';

const dayMonth = (props) => {
    const [eventList, setEventList] = useState([])

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

    const dayWrapper={
        width: `${props.cellWidth}px`,//here
        height: `${props.cellHeight}px`,
    };

    const clickDay = () => {
        props.setDate({
            year: props.data.date.getFullYear(),
            month:props.data.date.getMonth(),
            day: props.data.day,
            view: 'day'
        })
    }
    
    const containerStyle = {
        ...dayWrapper,
        backgroundColor: props.data.current 
                            ? 'white'
                            : 'transparent'
    }
    
    return(
        <div 
          className={styles.mobileDay} 
          style={containerStyle}
                   >    
            <div className={styles.label}>
                <span>
                    <h5>
                        {props.showDay  
                            ? <span onClick={clickDay}>{props.data.day}</span>
                            : <span>{props.data.day}</span>} 
                    </h5>
                </span>
            </div>
            <div className={styles.event_list}>
                {eventList.length < 3 
                    ? eventList.map((event, i) =>(
                        <Event 
                            width={props.width}
                            key={i} 
                            data={event}
                            view={props.view}
                        />))
                    : <HoverableEventList 
                        width={props.width}
                        view={props.view}
                        events={eventList}
                      />
                }
            </div>
        </div>
    )
}




export default dayMonth;