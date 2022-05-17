import React, {useState} from 'react'
import styles from './Day.css'
import Context from '../../container/provider';


const HoverableEventList = (props) =>{
    const [showEvents, setShowEvents] =  useState(false)
    

    return(
            <div> 
                <div 
                  style={{backgroundColor: props.context.primary}}
                  className={styles.eventBox}
                  onClick={()=> setShowEvents(true)}
                >
                    ({props.events.length}) Events
                </div>
                <div 
                  className={styles.hiddenEventsList} 
                  style={{display: showEvents ? 'block': 'none'}}
                >
                    <div className={styles.eventCard}>
                        <h3>Events: </h3>
                        <button 
                          className='btn'
                          onClick={()=>setShowEvents(false)}
                        >
                            <i className="fa fa-times" aria-hidden="true"></i>
                        </button>
                    </div>
                    {props.events.map((event) =>(
                    <a 
                      key={event.id}
                      href={event.id}>
                        <div
                          className={styles.eventBox + " mb-1"} 
                          style={{backgroundColor: props.context.primary}}
                        >
                            {event.title}
                        </div>
                    </a>))}
                </div>
        </div>)
}

const HoverableEventListHOC = (props) => (
  <Context.Consumer>{context => (
      <HoverableEventList {...props} context={context}/>
  )}</Context.Consumer>
)


export default HoverableEventListHOC