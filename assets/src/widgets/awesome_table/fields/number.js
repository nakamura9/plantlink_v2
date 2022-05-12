import React from 'react'
import {useState} from 'react'
import styles from './fields.css'
const numberStyles = {
    textAlign: "right"
}

const NumberField = (props) => {
    const onChange = (evt) => {
        props.onChange({
            target: {
                value: parseFloat(evt.target.value),
                name: props.name
            }
        })
    }
    return <input 
              type="number" 
              className={styles.table_input} 
              style={numberStyles}
              name={props.name} 
              onChange={onChange} 
              disabled={props.frozen}
              value={props.value}/>
}

const IntegerField = (props) => {
    const onChange = (evt) => {
        props.onChange({
            target: {
                value: parseInt(evt.target.value),
                name: props.name
            }
        })
    }
    return <input 
              type="number" 
              className={styles.table_input} 
              style={numberStyles}
            //   name={props.name} 
              onChange={onChange} 
              disabled={props.frozen}
              value={props.value}/>
}

export {NumberField, IntegerField}

