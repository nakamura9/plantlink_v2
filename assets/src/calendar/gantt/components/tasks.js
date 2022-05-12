/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {useEffect, useState} from 'react'
import styles from '../style.css'


const Tasks = (props) =>{
    return(
        <div className={styles.taskBarChart} style={{
            width: `${props.wingspan}px`,
            top: `${props.verticalOffset}px`,
            left: `${props.horizontalOffset}px`,
            }}>
            {props.tasks.map((task, i) =>{
                const leftOffset= parseInt(new Date(task.date) - props.start) / (24 * 60 * 60 * 1000)
                const width = task.span && task.span > 1 
                                ? (task.span + 1) * 48
                                : 48
                return(<div className={styles.taskBar}
                            style={{
                                backgroundColor: props.colors[i % 12],
                                width: `${width}px`,
                                left: `${(leftOffset * 48) - 4}px`
                                }}>
                </div>)
            })}
        </div>
    )
}

export default Tasks