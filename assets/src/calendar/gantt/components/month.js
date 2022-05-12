/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {useState, useEffect} from 'react'
import styles from '../style.css'
import moment from 'moment'

// Props 
//      month 
//      year
//      start number if null the first
//      end number if null the last day of the month

const month = (props) => {
    const first = new Date(`${props.month + 1}/1/${props.year}`)

    let last
    if(props.end && props.end.getMonth() != first.getMonth()){
        last = props.end
    }else{
        last = new Date(props.year, props.month + 1, 0)
    }

    let span =  moment(last).diff(moment(first), 'days') + 1
    if(span < 0) {
        span = moment(first).daysInMonth()
    }

    const data = new Map()
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    const day = 24 * 60 * 60 * 1000
    const days = new Array(span).fill(0).map((_, index) => new Date(first.getTime() + (day * index)))
    
    days.forEach(d => {
        const month = data.get(d.getMonth())
        if(!month) {
            data.set(d.getMonth(), [d])
        } else {
            month.push(d)
        }
    })

    return(
        <div className={styles.monthContainer}>
            {Array.from(data.keys()).map(month => (
                <div id="myID">
                    <div 
                      className={styles.monthHeader}
                      style={{width: `${48 * data.get(month).length}px`}}
                    >
                        <h4>{`${months[month]} ${data.get(month)[0].getFullYear()}`}</h4>
                    </div>
                    <div className={styles.ganttTable}>
                        <div className={styles.ganttTableRow}>
                            {data.get(month).map((date, i) => {
                                const val = date.getDate()
                                const today = props.year == props.today.getFullYear() &&
                                                props.month == props.today.getMonth() &&
                                                date == props.today 
                                return(
                                    <div 
                                      key={i}
                                      className={styles.ganttTableCell}
                                      style={{
                                            height: `${props.height - 160}px`,
                                            width: "48px",
                                            backgroundColor: today ? '#eee': 'white',
                                            borderLeftColor: today ? '#eee': 'white'
                                        }}>{val}</div>
                                        )
                                    })
                                }
                        </div>
                    </div>
                </div>
            ))}    
        </div>
    )
}


export default month
