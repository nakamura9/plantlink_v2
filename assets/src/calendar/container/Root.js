/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component, createContext} from 'react';
import Month from '../components/Month/Month';
import WeekView from '../components/Week/WeekView';
import DayView from '../components/Day/DayView';
import MenuBar from '../components/menu_bar';
import styles from './styles.css'
import Context from './provider'
import axios from 'axios';
import Gantt from '../gantt/root'
import PropTypes from 'prop-types';


/**
 * This application supports a variety of customizations
 * The hook system
 * ----------------
 * each view has certain hooks that allows you to feed events to the calendar
 * the hooks are the monthHook, weekHook and dayHook respectively.
 * The month hook takes 3 arguments, a year a month and the component.
 * It expects the hook to connect to an api and fetch events that are valid for 
 * that month and to set the state of the component's event state so as to 
 * update the window.
 * The week and day hooks work similarly. The primary difference is that the 
 * latter two take a day parameter in addition to the ones stated for the month 
 * hook.
 * 
 * Custom Params
 * -------------
 * In addition the interface can be tweaked using flags.
 * The first flag, showMonth allows us to hide the sidebar buttons for the 
 * month view.
 * similarly a showWeek and showDay flag are implemented.
 * The showDay flag however disables the links in the week and day views so 
 * that the user cannot open them. 
 * The eventLink flag takes a string and allows the creation of new events on a 
 * different page.
 * if flag is not set the create event button is removed from the interface.
 */



export default class CalendarApp extends Component{
    state = {
        year: 2018,
        month: 1,
        day: 1,
        view: 'month',
        appWidth: 0,
        appHeight: 0,
        menuHeight: 0,
        monthText: ""
    }

    propTypes = {
        layout: PropTypes.object,
        eventLink: PropTypes.string,
        showMonth: PropTypes.bool,
        showWeek: PropTypes.bool,
        showDay: PropTypes.bool,
        primaryColor: PropTypes.string.isRequired,
        accentColor: PropTypes.string.isRequired,
        monthHook: PropTypes.func,
        weekHook: PropTypes.func,
        dayHook: PropTypes.func,
        eventLink: PropTypes.string.isRequired
    }

    constructor() {
        super()
        this.containerRef = React.createRef()
        this.menuRef = React.createRef()
    }

    setMonthText = (text) =>{
        this.setState({
            monthText: text == undefined 
                ? this.getMonthText()
                : text
        })
    }

    getMonthText = () => {
        const dateString = new Date(this.state.year, this.state.month).toDateString()
        const dateArray = dateString.split(' ')
        return dateArray[1] + ' ' + dateArray[3]
    }

    componentDidUpdate(prevProps, prevState){
        if(prevState.month != this.state.month){
            this.setMonthText()
        }
    }

    nextHandler = () =>{
        const current = new Date(this.state.year, this.state.month, this.state.day)
        let next
        
        if(['month', 'gantt'].includes(this.state.view)){
            if(this.state.month < 11){
                next = new Date(this.state.year, this.state.month + 1, 1)
            }else{
                next = new Date(this.state.year + 1, 0, 1)
            }

        }else if(this.state.view == 'week'){
            current.setDate(current.getDate() + 7)
            next = current
        }else{
            current.setDate(current.getDate() + 1)
            next = current
        }

        this.setState({
            year: next.getFullYear(),
            month: next.getMonth(),
            day: next.getDate()
        })
    }

    prevHandler = () =>{
        const current = new Date(this.state.year, this.state.month, this.state.day)
        let next
        
        if(['month', 'gantt'].includes(this.state.view)){
            if(this.state.month != 0){
                next = new Date(this.state.year, this.state.month - 1, 1)
            }else{
                next = new Date(this.state.year - 1, 11, 1)
            }

        }else if(this.state.view == 'week'){
            current.setDate(current.getDate() - 7)
            next = current
        }else{
            current.setDate(current.getDate() - 1)
            next = current
        }
        this.setState({
            year: next.getFullYear(),
            month: next.getMonth(),
            day: next.getDate()
        })
    }

    componentDidMount(){
        // calculate the cell width
        // get the screen width
        // subtract the sidebar width
        // divide by 7
        // subtract the padding and border widths 
        // this.props.layout.setTitle("Calendar")
        const today = new Date()
        this.setState({
            day: today.getDate(),
            month: today.getMonth(),
            year: today.getFullYear(),
            appHeight: this.containerRef.current.clientHeight,
            menuHeight: this.menuRef.current.clientHeight,
            appWidth: this.containerRef.current.clientWidth,
        })
        this.setMonthText()
    }

    injectEvents = (month, year, comp) => {
        axios({
            method: "GET",
            url: `/planner/api/calendar/month/${year}/${month}/`,
            params: {
                app: this.props.app || "planner",
                model_name: this.props.model_name || "event"
            }
        }).then(res => {
            comp.setState({events: res.data})
        })
    }

    injectWeekEvents = (day, month, year, comp) => {
        axios({
            method: "GET",
            url: `/planner/api/calendar/week/${year}/${month}/${day}/`
        }).then(res => {
            comp.setState({events: res.data})
        })
    }

    injectDayEvents = (day, month, year, comp) => {
        axios({
            method: "GET",
            url: `/planner/api/calendar/day/${year}/${month}/${day}/`
        }).then(res => {
            comp.setState({events: res.data})
        })
    }

    render(){
        let rendered;
        switch(this.state.view){
            case 'month':
                rendered = <Month
                              width={this.state.appWidth}
                              // 8px for the 1px borders
                              cellWidth={(this.state.appWidth - 8) / 7}
                              // 8px for the 1px borders + 32px for the header
                              cellHeight={(this.state.appHeight - this.state.menuHeight - 60) / 6}
                              height={this.state.appHeight}
                              offsetTop={this.props.offsetTop}
                              params={{
                                month: this.state.month, 
                                year: this.state.year}}
                              showDay={this.props.showDay}
                              hook={this.injectEvents}
                              setDate={(params) =>{this.setState(params)}}
                            />;
                break;
            case 'week':
                rendered = <WeekView
                              width={this.state.appWidth / 7}
                              height={this.state.appHeight  - this.state.menuHeight - 60}
                              params={{
                                day: this.state.day,
                                month: this.state.month, 
                                year: this.state.year
                              }}
                              showDay={this.props.showDay}
                              setDate={(params) =>{this.setState(params)}}
                              hook={this.injectWeekEvents}
                              getMonthText={this.getMonthText}
                              setTitle={this.setMonthText}
                              />
                break;
            case 'day': 
                rendered = <DayView 
                              width={300}
                              height={this.state.appHeight  - this.state.menuHeight - 60}
                              params={{
                                    day: this.state.day,
                                    month: this.state.month, 
                                    year: this.state.year
                              }}
                              hook={this.props.dayHook}
                              setTitle={this.setMonthText}
                              hook={this.injectDayEvents}
                            />
                break;
            case 'gantt':
                rendered = <Gantt 
                             width={this.state.appWidth}
                             height={this.state.appHeight}
                             month={this.state.month}
                             year={this.state.year}
                             getData={this.injectEvents}
                            />
                break;
            default:
                rendered=<p>Loading Calendar...</p>
                break
        }

        return(
                <Context.Provider
                    value={{
                        primary: this.props.primaryColor,
                        accent:this.props.accentColor,
                        app:this.props.app,
                        model: this.props.model_name
                        }}>
                    <div className={styles.calendar} ref={this.containerRef}>
                        <div className={styles.renderedCalendar} >
                            <MenuBar
                              showDay={this.props.showDay}
                              menuRef={this.menuRef}
                              showMonth={this.props.showMonth}
                              showWeek={this.props.showWeek}
                              setView={(view)=>{
                                this.setState({view: view})
                              }}
                              nextHandler={this.nextHandler}
                              monthString={this.state.monthText}
                              prevHandler={this.prevHandler}
                              primary={this.props.primaryColor}
                              calendarState={{...this.state}}
                              eventLink={this.props.eventLink}

                            />
                            {/*App */}
                            {rendered}
                        </div>
                    </div>
                </Context.Provider>
        )
    }
    
}