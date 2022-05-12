import React from 'react'
import {useState} from 'react'
import styles from './fields.css'

const SelectField = (props) => {
    const onChange = (evt) => {
        // props.onChange(evt)
        props.onChange({
            target: {
                name: props.name,
                value: evt.target.value
            }
        })
    }
    return (
        <select 
          name={props.name} 
          className={styles.table_input} 
          value={props.value}
          onChange={onChange}
          disabled={props.frozen}
          >
            <option value={""}>----------</option>
            {props.options.map(opt => (<option key={opt[0]} value={opt[0]}>{opt[1]}</option>))}
        </select>
    )
}


export default SelectField