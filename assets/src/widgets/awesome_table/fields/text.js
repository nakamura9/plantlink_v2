import React from 'react'
import {useState} from 'react'
import styles from './fields.css'


const TextField = (props) => {
    const onChange = (evt) => {
        // props.onChange(evt)
        props.onChange({
            target: {
                name: props.name,
                value: evt.target.value
            }
        })
    }
    console.log("context")
    console.log(props.context)
    console.log(props.context == "form")
    if(props.context == "form") {
        return <textarea
                  rows={4}
                  cols={10}
                  className={styles.textarea}
                  name={props.name}
                  onChange={onChange} 
                  disabled={props.frozen}
                  value={props.value}
               >
                </textarea>
    }

    return <input 
              type="text" 
              className={styles.table_input}
              name={props.name} 
              onChange={onChange} 
              disabled={props.frozen}
              value={props.value}/>
}


const CharField = (props) => {
    const onChange = (evt) => {
        // props.onChange(evt)
        props.onChange({
            target: {
                name: props.name,
                value: evt.target.value
            }
        })
    }

    return <input 
              type="text" 
              className={styles.table_input}
              name={props.name} 
              onChange={onChange} 
              disabled={props.frozen}
              value={props.value}/>
}

export {TextField, CharField}