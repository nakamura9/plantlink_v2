/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React from 'react'
import axios from 'axios'
import Month from './components/month'
import TaskList from './components/task_list'
import TaskBarChart from './components/tasks'
import styles from './style.css'
import _ from 'lodash'
import SvgOverlay from './components/svgOverlay'
// Identify the start and end dates of the project. Then create a gantt view that spans that distance


class GanttChart extends React.Component{
    state = {
        today: new Date(),
        events: [
            {
                'description': "Something",
                span: 5,
                start: "02/05/2022"
            }
        ],
        start: new Date(),
        end: new Date(),
        duration: 50,
        events: [],
        leftBoundary: 0
    }

    colors = [
        '#007bff',
        'steelblue',
        'crimson',
        'darkred',
        'orangered',
        'fuchsia',
        'indigo',
        'lime',
        'lightseagreen',
        'deepskyblue',
        'lightslategray',
        'chocolate'
    ]

    constructor() {
        super() 
        this.leftScroller = React.createRef()
        this.rightScroller = React.createRef()
        this.monthsRef = React.createRef()
    }

    componentDidMount() {
        this.props.getData(this.props.month, this.props.year, this)
        this.setState({start: new Date(`${this.props.month + 1}/1/${this.props.year}`)})
        
        const me = this
        this.rightScroller.current.onmouseover = () => {
            me.rightScrollIntervalID = setInterval(() => {
                me.monthsRef.current.scrollLeft += 5
            }, 33)
        }

        this.rightScroller.current.onmouseleave = () => {
            if(!me.rightScrollIntervalID) return
            clearInterval(me.rightScrollIntervalID)
        }

        this.leftScroller.current.onmouseover = () => {
            me.leftScrollIntervalID = setInterval(() => {
                me.monthsRef.current.scrollLeft -= 5
            }, 33)
        }

        this.leftScroller.current.onmouseleave = () => {
            if(!me.leftScrollIntervalID) return
            clearInterval(me.leftScrollIntervalID)
        }

        this.setState({leftBoundary: this.monthsRef.current.offsetLeft})
    }

    componentDidUpdate(prevProps, prevState) {
        if(this.props.month != prevProps.month || this.props.year != prevProps.year) {
            this.props.getData(this.props.month, this.props.year, this)
            this.setState({start: new Date(`${this.props.month + 1}/1/${this.props.year}`)})
            console.log("Month update")
        }
        if(!_.isEqual(this.state.events, prevState.events)) {
            let max = this.state.start
            this.state.events.forEach(evt => {
                const date = new Date(evt.date)
                const end = new Date(date.getTime() + (evt.span * 24 * 60 * 60 * 1000))
                if(end > max) {
                    console.log("End")
                    max = end
                }
            })
            this.setState({end: max})
        }
    }

    render(){
        
        return(<React.Fragment>
            <div className={styles.chart} style={{width: '100%', overflowX: 'auto'}}>
                <TaskList 
                    tasks={this.state.events} 
                    colors={this.colors}
                    />
                <div 
                  className={styles.months}
                  style={{width: `${200}px`}}
                  ref={this.monthsRef}
                >
                    <div 
                      className={styles.scroll_left} 
                      ref={this.leftScroller}
                      style={{left: this.state.leftBoundary}}
                    ></div>
                    <TaskBarChart 
                        today={this.state.today}
                        start={this.state.start}
                        tasks={this.state.events} 
                        colors={this.colors}
                        verticalOffset={26 + 46} //do a better job
                        horizontalOffset={0}
                        wingspan={this.state.duration * 24}
                    />
                    <Month
                        month={this.props.month}
                        start={this.state.start}
                        end={this.state.end}
                        year={this.props.year}
                        tasks={this.state.events}
                        today={this.state.today}
                        width= {this.props.width - 250}
                        height={this.props.height}
                    />
                    <SvgOverlay 
                      width={this.props.width - 250}
                      height={this.props.height}
                      tasks={this.state.events} 
                    />
                    <div
                      className={styles.scroll_right} 
                      ref={this.rightScroller}
                    >
                    </div>
                </div>

        </div>
        </React.Fragment>)
    }
}

export default GanttChart