import React from 'react';
import {useState, useEffect, Component} from 'react'
import Header from '../table/header'
import Footer from '../table/footer'
import Body from '../table/body'
import styles from '../table/table.css'
import axios from 'axios'
import PropTypes from 'prop-types'
import getHook from '../hooks';
import _ from 'lodash'


/**
 * TODO: implement field level hooks
 */

 const dataParser = (data) => {
    if(data.schema && data.data) {
        const newData = data.data.map(row => {
            const newRow = {}
            Object.keys(row).forEach(k => {
                const field = data.schema.fields.filter(f => f.name == k)[0]
                if(field && field.fieldtype == 'number') {
                    newRow[k] = parseFloat(row[k])
                }else{
                    newRow[k] = row[k]
                }
            })
            return newRow            
        })
        data.data = newData
        return data
    }else {
        return data
    }
}


const dynamicSelectParser = (data, fields) => {
    const dynamicFields = fields.filter(f => f.type == "dynamic_search")
    if(dynamicFields.length == 0) {
        return data
    }
    const newData = [...data.data]
    newData.forEach(d => {
        dynamicFields.forEach(f => {
            if(d[f.options.modelname]) {
                d[f.name] = {
                    model: d[f.options.modelname],
                    instance: d[f.options.instancename]
                }
            }
        })
    })
    
    data.data = newData
    return data
}


class OneTable extends Component {
    static propTypes = {
        model_id: PropTypes.string,
        fields: PropTypes.array,
        inputID: PropTypes.string,
        readOnly: PropTypes.bool,
        editOnly: PropTypes.bool,
        editOnlyStrict: PropTypes.bool,
        addOnly: PropTypes.bool,
        onLineAdd: PropTypes.func,
        onLineEdit: PropTypes.func,
        onLineRemove: PropTypes.func,
        onUpdateInit: PropTypes.func,
        onChange: PropTypes.func
    }

    state = {
        data: [],
        editing: null,
        showPopup: false
    }

    constructor(props) {
        // For detecting clicks outside the boundary of the table
        // to clear any editing state.
        super(props)
        this.wrapperRef = React.createRef()
        this.handleClickOutside = this.handleClickOutside.bind(this)
    }

    handleClickOutside(event) {
        if( this.wrapperRef && 
            this.wrapperRef.current && 
            !this.wrapperRef.current.contains(event.target) &&
            !this.state.showPopup) {
            this.setState({editing: null})
        }
    }

    getInitial = () => {
        if(this.props.model_id && location.href.indexOf('update') != -1) {
            const url_parts = location.href.split('/')
            const id = url_parts[url_parts.length - 2]
            const [app, model] = this.props.model_id.split('.')
            const tableIndex = this.props.tabIndex || 0
            console.log(id)
            axios.get(`/api/child-table/${app}/${model}/${id}?tabindex=${tableIndex}`)
                .then(res => {
                    console.log(res)
                const data = dynamicSelectParser(dataParser(res.data), this.props.fields)
                this.setState({data: data.data}, () => {
                    setTimeout(this.handleChange, 100)
                })
            })
        }
    }

    componentDidMount() {
        document.addEventListener('mousedown', this.handleClickOutside)
        this.getInitial()
        window.form = window.form || {}
        setTimeout(this.onValidationError.bind(this), 250)
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside)
        delete window.form[this.varname]
    }

    onValidationError() {
        if(!this.props.inputID) { return }
        const dataObj = document.getElementById(this.props.inputID)
        if(this.state.data.length == 0 && dataObj.value.length > 0) {
            this.setState({data: JSON.parse(decodeURIComponent(dataObj.value))})
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(!_.isEqual(this.state.data,  prevState.data)) {
            if(this.props.inputID) {
                this.updateForm()
            }
        }
        if(prevProps.tabIndex != this.props.tabIndex) {
            this.getInitial()
            if(window.form.table) {
                this.varname = 'table_' + this.props.tabIndex
                window.form[this.varname] = this
            } else {
                this.varname = "table"
                window.form.table = this
            }
        }
    }

    handleChange = () => {
        if(this.props.onChange) {
            this.props.onChange(
                `child_table${this.props.tabIndex > 0 ? this.props.tabIndex : ""}`, 
                encodeURIComponent(JSON.stringify(this.state.data))
            )
        }
    }

    addRow = (item) => {
        const newData = [...this.state.data]
        newData.push(item)
        this.setState({data: newData}, () => {
            const hook = getHook(this.props.tabIndex || 0, 'onLineAdd')
            if(hook) {
                hook(item, this)
            }
            // deprecated
            if(this.props.onLineAdd) {
                this.props.onLineAdd(item, this)
            }
            // timeout to ensure both states are updated...
            // TODO find a better solution.
            setTimeout(this.handleChange, 100)
        })
    }

    deleteRow = (rowID) => {
        const newData = [...this.state.data]
        newData.splice(rowID, 1)
        this.setState({data: newData}, () => {
            const hook = getHook(this.props.tabIndex || 0, 'onLineRemove')
            if(hook) {
                hook(this)
            }
            // deprecated
            if(this.props.onLineRemove) {
                this.props.onLineRemove(this)
            }

            // timeout to ensure both states are updated...
            // TODO find a better solution.
            setTimeout(this.handleChange, 100)
        })

    }

    editRow = (rowID, row) => {
        const newData = [...this.state.data]
        newData.splice(rowID, 1, row)
        this.setState({
            data: newData
            // editing: null
        }, () => {
            const hook = getHook(this.props.tabIndex || 0, 'onLineEdit')
            if(hook) {
                hook(row, rowID, this)
            }
            // deprecated
            if(this.props.onLineEdit) {
                this.props.onLineEdit(row, rowID, this)
            }

            // timeout to ensure both states are updated...
            // TODO find a better solution.
            setTimeout(this.handleChange, 100)
        })
    }

    editRowToggle = (rowID) => {
        this.setState({editing: rowID})
    }

    togglePopup = () => {
        this.setState({showPopup: !this.state.showPopup})
    }

    updateForm = () => {
        const formInput = document.getElementById(this.props.inputID)
        formInput.value = encodeURIComponent(JSON.stringify(this.state.data))
    }

    render() {
        if(!this.props.fields) { return <h4>Loading...</h4> }
        return (
            <div className={styles.mobileWrapper + " mb-3"}>
                <table className={styles.table} ref={this.wrapperRef}>
                    <Header fields={this.props.fields}/>
                    <Body 
                        fields={this.props.fields} 
                        readOnly={this.props.readOnly}
                        editOnlyStrict={this.props.editOnlyStrict}
                        addOnly={this.props.addOnly}
                        data={this.state.data} 
                        editing={this.state.editing}
                        editRowToggle={this.editRowToggle}
                        editRow={this.editRow}
                        deleteRow={this.deleteRow}
                        togglePopup={this.togglePopup}
                        tabIndex={this.props.tabIndex || 0}
                        />
                    {this.props.readOnly || this.props.editOnly 
                        ? null
                        : <Footer 
                            fields={this.props.fields}
                            editing={this.state.editing} 
                            addRow={this.addRow}
                            readOnly={this.props.readOnly}
                            togglePopup={this.togglePopup}
                            tabIndex={this.props.tabIndex || 0}
                        />}
                </table>
                {/* <PopupForm 
                  show={this.state.showPopup} 
                  togglePopup={this.togglePopup}
                  fields={this.props.fields}
                  addRow={this.addRow}
                  editRow={this.editRow}
                  rowID={this.state.data.length + 1}
                  data={this.state.data}
                  editing={this.state.editing}
                  tabIndex={this.props.tabIndex || 0}
                /> */}
            </div>
        )
    }
}


export default OneTable