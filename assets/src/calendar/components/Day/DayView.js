/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import Event from '../Event';
import Context from '../../container/provider'
import _ from 'lodash'
import {intervals} from '../Week/WeekView'
import weekStyles from '../Week/week.css'


class DayView extends Component{
    state = {
        date: "",
        events: [],
        width: 480
    }

    componentDidUpdate(prevProps, prevState){
        if(! _.isEqual(this.props.params, prevProps.params)){
            this.updateCalendar()
        }
    }

    updateCalendar =() =>{
        const params = this.props.params 
        this.setState({
            date: new Date(params.year, params.month, params.day).toDateString()
        }, () => this.props.setTitle(this.state.date))

        this.props.hook(params.day, params.month, params.year, this)
    }

    componentDidMount(){
        this.updateCalendar()
    }

    render(){
    
    // only week and day views have an hourly breakdown therefore only two 
    // options
   
        const dayWrapper = {
            width: `${this.state.width}px`,
            height: this.props.height + 'px',
            padding: '0px',
            marginLeft: "20px"
        } 
        
        // do some overlap detection
        return(
            <Context.Consumer>{context=>(
                <div style={dayWrapper}>
                    <div className="card shadow">
                        <div className="card-body">
                            <div 
                                style={{
                                    position: "relative",
                                    width: "100%",
                                }}>
                            {intervals.map(int => (
                                <div className={weekStyles.interval}>
                                    <span >{int}</span>
                                </div>
                            ))}
                            {this.state.events.map((event, i) =>(
                                <Event
                                    index={1 + i}
                                    offset={50 * (i % 3)}
                                    width={this.state.width}
                                    key={i} 
                                    data={event}
                                    view={"day"}/>
                            ))}
                            </div>
                        </div>
                    </div>
                </div>
                
            )}</Context.Consumer>
    )
    }    
}

export default DayView;