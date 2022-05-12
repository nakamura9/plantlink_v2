import React from 'react'
import {useState} from 'react'

const BooleanField = (props) => {
    const onChange = (evt) => {
        props.onChange({
            target: {
                value: evt.target.checked,
                name: props.name
            }
        })
    }
    return  <div style={{display:'flex', justifyContent: 'center'}}>
        <input 
                type="checkbox"
                onChange={onChange}
                name={props.name}
                checked={props.value}
                disabled={props.frozen}/>
    </div>
}

export default BooleanField