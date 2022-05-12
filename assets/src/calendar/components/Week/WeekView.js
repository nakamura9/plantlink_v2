/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import Day from '../Day/Day';
import styles from './week.css';
import {showWeekCalendar} from '../../calendar'
import moment from 'moment'
import Context from '../../container/provider';
import _ from 'lodash'

const intervals = ['00:00', '01:00', '02:00', '04:00', '05:00', '06:00', 
    '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', 
    '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
    '21:00', '22:00', '23:00'  
]

const days = [
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
]

class WeekView extends Component{
    state = {
        week: "",
        days: [],
        events: []
    }

    componentDidUpdate(prevProps, prevState){
        if(! _.isEqual(prevProps.params, this.props.params)){
            this.updateCalendar()
        }
    }

    updateCalendar(){
        const params = this.props.params 
        const currWeek = showWeekCalendar(params.day, params.month, params.year)
        const m = moment(new Date(params.year, params.month, params.day))
        
        this.setState({
            days: currWeek,
            week: m.week()
        }, () => this.props.setTitle(`${this.props.getMonthText()}, Week: ${this.state.week}`))
        
        this.props.hook(params.day, params.month, params.year, this)
    }

    componentDidMount(){
        this.updateCalendar()
    }

    render(){
        if(this.state.days.length === 0){
            return(<h3>Loading data...</h3>)
        }
    
        return(
            <Context.Consumer>
                {context =>{
                    const bgStyle = {backgroundColor: context.primary}
                return (
                    <React.Fragment>
                        <div 
                            style={{height: `${this.props.height}px`}}
                            className={styles.weekContainer}
                        >
                            <div className={styles.underLay}>
                                <div className={styles.days} style={bgStyle}>
                                    {days.map(d => <div style={{width:this.props.width}}>{d}</div>)}
                                </div>
                                {intervals.map(int => (
                                    <div className={styles.interval}>
                                        <span >{int}</span>
                                    </div>
                                ))}
                            </div>
                            <div className={styles.overLay}>
                                {this.state.days.map((day, i) =>(        
                                        <Day
                                            data={{...day, current: true}}
                                            setDate={this.props.setDate}
                                            view={'week'} 
                                            width={this.props.width}
                                            height={this.props.height}
                                            events={this.state.events}
                                            showDay={this.props.showDay}
                                            />))}
                            </div>
                        </div> 
                    </React.Fragment>
                )}
            }
            </Context.Consumer>
        )
    }
}
    

export default WeekView;
export {intervals}