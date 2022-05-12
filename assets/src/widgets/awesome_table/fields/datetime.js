import React from 'react'
// import TimeInput from '../../components/time_field'
import {useState} from 'react'
import styles from './fields.css'
import DatePicker from 'react-datepicker'
require("react-datepicker/dist/react-datepicker.css")

const DateField = (props) => {
    const onChange = (value) => {
        props.onChange({
            target: {
                value: value.toISOString().slice(0, 10),
                name: props.name
            }
        })
    }
    
    return <div className={styles.dateInput}>
        <DatePicker 
              showMonthDropdown
              showYearDropdown
              dropdownMode="select"
              selected={props.value ? new Date(props.value) : props.value}
              onChange={onChange}
              readOnly={props.frozen}
            />
    </div> 
}

// const TimeField = (props) => {
//     const onChange = (data, name) => {
//         props.onChange({
//             target: {
//                 name: props.name,
//                 value: data.value
//             }
//         })
//     }
//     return <TimeInput 
//              name={props.name}
//              initial={props.value}
//              handler={onChange}/>
// }


export default DateField