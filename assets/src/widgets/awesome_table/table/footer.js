import React from 'react'
import {InputRow} from '../table/rows'

const Footer = (props) => {
    return(
        <tfoot>
            {props.editing == null 
                ? <InputRow 
                    fields={props.fields}
                    addRow={props.addRow}
                    togglePopup={props.togglePopup}
                    tabIndex={props.tabIndex}
                    /> 
                : null}
        </tfoot>
    )
}

export default Footer;