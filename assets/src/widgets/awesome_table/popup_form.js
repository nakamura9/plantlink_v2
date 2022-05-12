import React, {Component} from 'react'; 
import styles from './popup_style.css';
import {EditableBase, setInitial} from './table/rows'
import renderField from './fields/render'
import Modal from '../components/modal';


class PopUpForm extends EditableBase {
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
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(this.props.editing != null && 
                this.props.editing != prevProps.editing) {
            const inputData = {}
            this.props.fields.forEach(field => {
                const rowData = this.props.data[this.props.editing]
                inputData[field.name] = rowData[field.name]
                if(field.type == "search") {
                    inputData[field.name + "_id"] = rowData[field.name + "_id"]
                }else if (field.type == "dynamic_search") {
                    inputData[field.options.modelname] = rowData[field.options.modelname]
                    inputData[field.options.instancename] = rowData[field.options.instancename]
                }
            })
            this.setState({inputData: inputData})
        }
    }

    confirmEdit = () => {
        const [valid, missing] = this.rowValidate()
        if(!valid) {
            bentschAlert(`Invalid row. ${missing} field is missing.`)
            return
        }
        this.props.editRow(this.props.editing, this.state.inputData)
        this.props.togglePopup()
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

    buttonHandler = () => {
        if (this.props.editing == null ) {
            this.addRowHandler()
        } else {
            this.confirmEdit()
        }
    }

    render() {
        return (
            <Modal
              handleClose={this.props.togglePopup}
              show={this.props.show}
              title={`Row # ${ this.props.editing == null ? this.props.rowID : this.props.editing + 1}`}
            >
                {this.state.resetFlag
                        ? null 
                        : this.props.fields.map(field =>  (
                            <div key={field.name}>
                                <label>{field.label}:</label>
                                <div className={styles.fieldbox}>
                                    {renderField(
                                        field, 
                                        field.type == "search" 
                                            ? this.state.inputData[field.name + "_id"]
                                            : this.state.inputData[field.name], 
                                        this.inputHandler,
                                        "form"
                                    )}
                                    </div>
                            </div>))
                    }
                    <button
                      className="btn btn-primary"
                      type="button"
                      onClick={this.buttonHandler}
                    >
                        {this.props.editing == null ? "Add" : "Edit"} Row
                    </button>
            </Modal>
        )
    }
}

export default PopUpForm