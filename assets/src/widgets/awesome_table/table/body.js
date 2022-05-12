import React from 'react'
import {DisplayRow, EditRow} from './rows'

const Body = (props) => {
    if(props.addOnly) {
        return (
            <tbody>
                 {props.data.map((row, i) => (
                    <DisplayRow 
                        data={row} 
                        fields={props.fields} 
                        idx={i} 
                        key={i}
                        readOnly
                        editRowToggle={props.editRowToggle}    
                        removeHandler={props.deleteRow}/>
                    ))}
            </tbody>
        )
    }
    return (
        <tbody>
            {props.data.map((row, i) => (
                i == props.editing
                    ? <EditRow 
                        data={row}
                        fields={props.fields}
                        idx={i} 
                        key={i}
                        editRow={props.editRow}
                        togglePopup={props.togglePopup}
                        tabIndex={props.tabIndex}/>
                    : <DisplayRow 
                        data={row} 
                        fields={props.fields} 
                        idx={i} 
                        key={i}
                        readOnly={props.readOnly}
                        togglePopup={props.togglePopup}
                        editOnlyStrict={props.editOnlyStrict}
                        editRowToggle={props.editRowToggle}
                        
                        removeHandler={props.deleteRow}/>
            ))}
        </tbody>
    )
}

export default Body