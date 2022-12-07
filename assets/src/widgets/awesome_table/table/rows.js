import React, { Component } from 'react'
import renderData from '../tools'
import renderField from '../fields/render'
import styles from './table.css'
import getHook from '../hooks'
import _ from 'lodash'

const setInitial = (fieldType) => {
    switch(fieldType) {
        case 'number':
            return 0.0
        case 'text': 
            return ""
        default:
            return null;
    }
}

class EditableBase extends Component {
    rowValidate = () => {
        let valid = true;
        let missing_field = null;
        for(let f of this.props.fields) {
            const value = this.state.inputData[f.name]
            if(f.required && !value && value != 0  ) {
                valid = false;
                missing_field = f.label
                break;
            }
        }
        return [valid, missing_field]
    } 

    // deprecated
    propsInputHandler = (field, evt, newInputData) => {
        if(field.asyncFieldHandler != undefined) {
            field.asyncFieldHandler(evt.target.value, newInputData)
                .then(res => {
                    this.setState({inputData: res})
                })
        } else {
            if(field.fieldHandler != undefined) {
                newInputData = field.fieldHandler(evt.target.value, newInputData)
            }
            this.setState({inputData: newInputData})
        }
    }

    inputHandler = (evt) => {
        let newInputData = {...this.state.inputData}
        // for dynamic fields
        if(evt.hasOwnProperty('dynamicField')) {
            // goal: map model_field to value, map instance_field to value
            newInputData[evt.modelname] = evt.model // modelname to model
            newInputData[evt.instancename] = evt.instance // instancename to instance
            newInputData[evt.fieldname] = evt.field
            this.setState({inputData: newInputData})
            const field = this.props.fields.filter(f => f.name == evt.fieldname)[0]
            const hook = getHook(this.props.tabIndex, field.name)
            const async_hook = getHook(this.props.tabIndex, "async_" + field.name)
            if(hook != undefined) {
                hook(evt.field, newInputData)
                this.setState({inputData: newInputData})
            }
            if(async_hook != undefined) {
                async_hook(evt.field, newInputData)
                    .then(res => {
                        this.setState({inputData: res})
                    })
            }
            
        } else {
            newInputData[evt.target.name] = evt.target.value
            if(evt.target.valueID != undefined) {
                newInputData[evt.target.name + '_id'] = evt.target.valueID
            }
            const field = this.props.fields.filter(f => f.name == evt.target.name)[0]
            
            const hook = getHook(this.props.tabIndex, field.name)
            const async_hook = getHook(this.props.tabIndex, "async_" + field.name)
            if(hook != undefined) {
                hook(evt.target.value, newInputData)
                this.setState({inputData: newInputData})
            }
            if(async_hook != undefined) {
                async_hook(evt.target.value, newInputData)
                    .then(res => {
                        this.setState({inputData: res})
                    })
            }
            // deprecated
            this.propsInputHandler(field, evt, newInputData)
        }
        
    }
}


class InputRow extends EditableBase {
    constructor(props) {
        super()
        const inputData = {}
        props.fields.forEach(field => {
            inputData[field.name] = setInitial(field.type)
            if(field.type == "search") {
                inputData[field.name + "_id"] = null
            }
        })
        this.state = {
            inputData: inputData,
            resetFlag: false,
            showEllipsis: false
        }
    }

    addRowHandler = () => {
        const [valid, missing] = this.rowValidate()
        if(!valid) {
            bentschAlert(`Invalid row. ${missing} field is missing.`)
            return
        }
        this.props.addRow(this.state.inputData)
        const inputData = {}
        this.props.fields.forEach(field => {
            inputData[field.name] = setInitial(field.type)
        })
        this.setState({
            resetFlag: true,
            inputData: inputData
        })
        setTimeout(() => this.setState({resetFlag: false}), 100)
    }

    render() {
        return (
            <React.Fragment>
                {this.state.resetFlag 
                    ? null
                    : <React.Fragment>
                        <tr className={styles.rows}
                            onMouseEnter={() => this.setState({showEllipsis: true})}
                            onMouseLeave={() => this.setState({showEllipsis: false})} >
                            <td>
                                <div className={styles.fill}>
                                    
                                </div>
                            </td>
                            {this.props.fields.filter(f => !f.hidden).map(field =>  (
                                <td key={field.name}>{renderField(
                                                        field, 
                                                        field.type == "link" 
                                                          ? this.state.inputData[field.name + "_id"]
                                                          : this.state.inputData[field.name], 
                                                        this.inputHandler,
                                                        "table")}</td>))}
                        </tr>
                        <tr className={styles.rows}>
                            <td></td>
                            <td colSpan={this.props.fields.length}>
                                <button 
                                  type="button" 
                                  className="btn btn-outline btn-xs add-row-btn" 
                                  onClick={this.addRowHandler}>Add Row</button>
                            </td>
                        </tr>
                    </React.Fragment>}
            </React.Fragment>)
    }
}


class EditRow extends EditableBase {
    constructor(props) {
        super()
        const inputData = {}
        props.fields.forEach(field => {
            inputData[field.name] = props.data[field.name]
            if(field.type == "link") {
                inputData[field.name + "_id"] = props.data[field.name + "_id"]
            }else if (field.type == "dynamic_search") {
                inputData[field.options.modelname] = props.data[field.options.modelname]
                inputData[field.options.instancename] = props.data[field.options.instancename]
            }
        })
        this.state = {
            inputData: inputData
        }
    }

    confirmEdit = () => {
        const [valid, missing] = this.rowValidate()
        if(!valid) {
            bentschAlert(`Invalid row. ${missing} field is missing.`)
            return
        }
        this.props.editRow(this.props.idx, this.state.inputData)
    }

    componentDidUpdate(prevProps, prevState){
        if(!_.isEqual(prevState.inputData, this.state.inputData)) {
            this.props.editRow(this.props.idx, this.state.inputData)
        }
    }

    render() {
        return (
            <tr className={styles.rows} >
                <td>
                    <div className={styles.fill}>
                         <button 
                            onClick={this.props.togglePopup} 
                            className={styles.expandButton}
                            type="button">
                        <i className="fa fa-expand" aria-hidden="true"></i>
                        </button>
                    </div>
                </td>
                {this.props.fields.filter(f => !f.hidden).map(
                    field => (<td key={field.name}>{
                                    renderField(field, 
                                                field.type == "link" 
                                                    ? this.state.inputData[field.name + "_id"]
                                                    : this.state.inputData[field.name], 
                                                 this.inputHandler)
                                    }
                                </td>))}
            </tr>
        )
    }
}

const DisplayRow = (props) => {
    const handleButtonClick = (evt) => {
        evt.stopPropagation()
        props.removeHandler(props.idx)
    }

    const handleRowClick = () => {
        if(props.readOnly) { return }
        props.editRowToggle(props.idx)
    }

    return (
        <tr onClick={handleRowClick} className={styles.rows}>
            <td>
                {props.readOnly || props.editOnlyStrict
                    ? null
                    : <button 
                        className={styles.inlineButton}
                        onClick={handleButtonClick}
                        type="button">
                            <i className="fa fa-times" aria-hidden="true"></i>
                        </button>}
            </td>
            {props.fields
                .filter(f => !f.hidden)
                .map(field => (<td key={field.name}>
                    {renderData(field, props.data[field.name], props.data)}
                    </td>))}
        </tr>
    )
}

export {DisplayRow, InputRow, EditRow, EditableBase, setInitial}