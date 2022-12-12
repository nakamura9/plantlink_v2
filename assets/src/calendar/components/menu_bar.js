import React from 'react';
import styles from './menu.css'
import MiniCalendar from '../components/mini_calendar';


const menuBar = (props) => {
    return (
        <div className={styles.menu_root} ref={props.menuRef}>
            <div className={styles.menu_container}>
                <div className={styles.right_aligned}>
                    {props.eventLink 
                        ? <a 
                            href={props.eventLink}
                            className="btn text-white create-btn"
                            style={{backgroundColor: props.primary}}
                        >
                                <i className="fas fa-plus"></i>  <span className={styles.createText}>Create New</span>
                        </a>
                        : null}
                    <h4> | {props.monthString}</h4>
                </div>
                <div>
                    <div className="btn-group mr-3">            
                        
                        <button 
                            className="btn text-white month-btn"
                            style={{backgroundColor: props.primary}}
                            onClick={props.toggleFilters}
                            
                        >
                            <i className="fas fa-filter"></i>
                        </button>
                        {props.showMonth ? 
                            <button className="btn text-white month-btn"
                            style={{backgroundColor: props.primary}}
                            onClick={()=>{props.setView('month')}}><i className="fas fa-calendar"></i> Month</button>:null}
                        {props.showWeek ?
                            <button className="btn text-white week-btn" 
                            style={{backgroundColor: props.primary}}
                            onClick={()=>{props.setView('week')}}> Week</button> : null}
                        {props.showDay ?
                            <button className="btn text-white day-btn" 
                            style={{backgroundColor: props.primary}}
                            onClick={()=>{props.setView('day')}}> Day</button>:null}
                    </div>

                    <button
                      style={{backgroundColor: props.primary}}
                      className="btn text-white mr-3 gantt-btn"
                      onClick={()=>{props.setView('gantt')}}
                    >
                            Gantt
                    </button>

                    <div className="btn-group mr-3">
                        <button
                            className="btn text-white navigate-left"
                            style={{backgroundColor: props.primary}}
                            onClick={props.prevHandler}>
                                <i className="fas fa-arrow-left"></i>
                        </button>    
                        <button
                            style={{backgroundColor: props.primary}}
                            className="btn text-white navigate-right"
                            onClick={props.nextHandler}>
                                <i className="fas fa-arrow-right"></i>
                        </button>
                    </div>
                    
                </div>
            </div>
        </div>
    )
}

export default menuBar 