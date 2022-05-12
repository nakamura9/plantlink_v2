/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React from 'react';
import Day from '../Day/DayMonth';
import styles from './week.css';

const week = (props) => {
    
    return(
        <tr>
            {props.days.map((day, i) =>(
                <td key={i}
                    className={styles.cellStyle}>
                    <Day 
                        offsetTop={props.offsetTop}
                        cellHeight={props.cellHeight}
                        cellWidth={props.cellWidth}
                        width={props.width}
                        data={day}
                        events={props.events} 
                        view='month'
                        setDate={props.setDate}
                        showDay={props.showDay}/>
                </td>
            ))}
        </tr>
    )
    
}

export default week;