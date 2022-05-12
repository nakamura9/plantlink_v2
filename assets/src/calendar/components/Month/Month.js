/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import Week from '../Week/Week';
import styles from './month.css';
import {showCalendar} from '../../calendar'
import Context from '../../container/provider'

class Month extends Component{
    state = {
        weeks: [],
        period: "",
        events: []
    }

    componentDidUpdate(prevProps, prevState){
        if(prevProps.params != this.props.params){
            this.updateCalendar()
        }
    }

    updateCalendar(){
        const params = this.props.params
        const data = showCalendar(params.month, params.year)
        this.setState({
            weeks: data,
            period: 'Period',
        })
        // inject events here!
        this.props.hook(params.month, params.year, this)
    }
    
    componentDidMount(){
        this.updateCalendar()
    }

    render(){
        return(
            <Context.Consumer>{context=>(
                <React.Fragment>
                {this.state.weeks.length != 0 
                    ? <table>
                        <thead>
                            <tr style={{backgroundColor: context.primary}}>
                                <th className={styles.header}>Sunday</th>
                                <th className={styles.header}>Monday</th>
                                <th className={styles.header}>Tuesday</th>
                                <th className={styles.header}>Wednesday</th>
                                <th className={styles.header}>Thursday</th>
                                <th className={styles.header}>Friday</th>
                                <th className={styles.header}>Saturday</th>
                            </tr>
                        </thead>
                        <tbody>
                        {this.state.weeks.map((week, i)=>(
                            <Week 
                                offsetTop={this.props.offsetTop}
                                cellWidth={this.props.cellWidth}
                                cellHeight={this.props.cellHeight}
                                width={this.props.width}
                                key={i} 
                                days={week}
                                events={this.state.events}
                                setDate={this.props.setDate}
                                showDay={this.props.showDay}/>
                        ))}
                        </tbody>
                      </table>
                    : <h1>Loading data...</h1> }
                </React.Fragment>
            )}</Context.Consumer>
        );
    }
    
    
}

export default Month;