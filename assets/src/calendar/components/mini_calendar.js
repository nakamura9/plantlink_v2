/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import Radium from 'radium';
import styles from './mini_calendar.css';
import {showCalendar} from '../calendar'
import Context from '../container/provider'

class  MiniCalendar extends Component{
    state = {
        weeks: []
    }
    
    componentDidUpdate(prevProps, prevState){
        if(this.props.year !== prevProps.year || prevProps.month !== this.props.month){
            const data = showCalendar(this.props.month, this.props.year)
            this.setState({
                weeks: data
                })
        }
    }
    
    render(){
        return(
            <Context.Consumer>{context=>(
                <div className={styles.calendar}>
            <h4 className={styles.title}>{this.props.monthString}</h4>
            <table className={styles.miniTable}>
                <tbody>
                    <tr>
                        <th>Mo</th>
                        <th>Tu</th>
                        <th>We</th>
                        <th>Th</th>
                        <th>Fr</th>
                        <th>Sa</th>
                        <th>Su</th>
                    </tr>
                    {this.state.weeks.length === 0
                        ? <tr>
                            <td colSpan={7}>Loading data...</td>
                        </tr>
                        : null
                    }
                    {this.state.weeks.map((week, i) =>(
                        <tr key={i}>

                            {week.map((day, j) =>(
                                <td key={j} style={{padding:'3px'}}>
                                    <a key={i.toString() + '-' + j.toString()}
                                        href={`/calendar/day/${day.date.getFullYear()}/${day.date.getMonth()+1}/${day.day}`}
                                        style={{
                                            textDecoration: "none",
                                        color: (i==0 && day.day > 7) || (i > 3 && day.day < 10)
                                        ? context.primary
                                        : 'white' ,
                                        width:" 100%",
                                        display: 'inline-block',
                                        ":hover": {
                                            color: context.primary,
                                            backgroundColor: 'white'
                                        }
                                    }}>{day.day}</a></td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            </div>
            )}</Context.Consumer>
        );
    }
}



export default Radium(MiniCalendar);