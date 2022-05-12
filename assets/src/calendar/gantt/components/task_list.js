/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React from 'react'
import styles from '../style.css'

const Task =(props) =>{
    return(
        <div className={styles.taskCard}
                style={{backgroundColor: props.color}}>
        {props.title.length > 20 
            ? props.title.slice(0,20) + '...'
            : props.title
        }
    </div>
    )
}


const Tasks = (props) =>{
    
    return(
        <div className={styles.taskList}>
            <div>
                <div className={styles.monthHeader}>
                    <h4>Events</h4>
                </div>
                <div style={{paddingTop: '26px'}}>
                    {props.tasks.map((task, i) =>{
                        return(<Task {...task} color={props.colors[i % 12]} key={i}/>)
                    })}
                </div>
            </div>
        </div>
    )
}



export default Tasks