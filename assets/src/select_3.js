/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import React, {Component} from 'react';
import axios from 'axios';
import styles from './select_3.css';
import Radium from 'radium';
import ReactDOM from 'react-dom';
/**
    Props
    -------

    toggleClear - bool
    app - string
    model - string
    onClear - function
    onSelect - function
    initial - string (pk)
    filters - object
    value - string (pk) -> changes state of input with changes in value
 */

const randomID = () => {
    return Math.random().toString(36).substring(7)
}

class SelectThree extends Component {
    state = {
        inputVal: "",
        selected: null,
        selection_list: [],
        options: [],
        filteredOptions: [],
        showOptions: false,
        disabled: false,
        filters: {}
    }


    componentDidUpdate(prevProps, prevState) {
        if(this.state.selected != prevState.selected && this.state.showOptions) {
            this.setState({showOptions: false})
        }
        if(this.props.toggleClear && this.props.toggleClear != prevProps.toggleClear) {
            this.setState({
                inputVal: "",
                filteredOptions: this.state.options,
                selected: null
            })
        }
        if(this.props.value && this.props.value != this.state.selected) {
            const selectedText = this.state.options 
                ? this.state.options.filter(opt => opt[0] == parseInt(this.props.value))[0][1]
                : ""
            this.setState({
                selected: this.props.value,
                inputVal: selectedText
            })   
        }

        if(this.props.filters != prevProps.filters || this.state.filters != prevState.filters) {
            if(this.props.filters != prevProps.filters) {
                let filters = this.props.filters
                if(typeof(filters) == "string") {
                    try {
                        filters = JSON.parse(filters)
                    } catch (err) {
                        filters = {}
                    }
                }
                this.setState({filters: filters}, () =>{
                    this.refreshOptions(null)
                })
            }else {
                this.refreshOptions(null)
            }
        }

        if(this.state.selected != prevState.selected) {
            $(`input[name="${this.props.name}"]`).trigger('change')
        }

        if(this.props.initial != prevProps.initial) {
            this.refreshOptions(this.props.initial)
        }
    }

    refreshOptions = (initial) => {
        axios({
            'method': 'GET',
            url: `/api/model-items/${this.props.app}/${this.props.model}/`,
            data: {
                filters: this.state.filters
            }
        }).then((resp) =>{
            this.setState({
                options: resp.data.data,
                filteredOptions: resp.data.data,
            }, () => {
                if(this.props.initial && initial) {
                    if(this.props.multiple) {
                        const selection = this.props.initial.map(idx =>{
                            return([idx, resp.data.data.filter(opt => opt[0] == idx)[0][1]])
                        })
                        this.setState({
                            selection_list: selection,
                            inputVal: ""
                        })  
                    } else {
                        
                        const selectedText = resp.data.data.filter(opt => opt[0] == this.props.initial)[0][1]
                        this.setState({
                            selected: this.props.initial,
                            inputVal: selectedText
                        })
                    }
                    
                }})
        })
        if(this.props.name) {
            if(!window.form) {
                window.form = {}
            }
            window.form[this.props.name + '_widget'] = this
        }
        
    }

    componentDidMount() {
        this.refreshOptions(true)
        if(this.props.disabled) {
            this.setState({disabled: this.props.disabled})
        }
        let filters = this.props.filters
        if(typeof(filters) == "string") {
            try {
                filters = JSON.parse(filters)
            } catch (err) {
                filters = {}
            }
        }
        this.setState({filters: filters || {}})
        if(this.props.initial) {
            $(`input[name="${this.props.name}"]`).trigger('change')
        }
    }

    handleInputChange = (evt) => {
        if(evt.target.value == "" && this.state.selected) {
            if(this.props.onClear) {
                this.props.onClear()
            }
            this.setState({
                filteredOptions: this.state.options,
                inputVal: "",
                selected: null
            }, () => $(`input[name="${this.props.name}"]`).trigger('change'))
            return
        }
        let selected = null
        const newOptions = this.state.options.filter(opt =>{
            if(opt[1] === evt.target.value) {
                selected = opt[0]
            } 
            return opt[1].toLowerCase().indexOf(evt.target.value.toLowerCase()) !== -1 
        })
        this.setState({
            filteredOptions: newOptions,
            inputVal: evt.target.value,
            selected: selected ? selected : this.state.selected
        }, () => { 
            if(!this.props.name) { return }
            const target = document.querySelector(`input[name="${this.props.name}"]`)
            const event = new Event('change');
            target.dispatchEvent(event);
        })
    }

    clearSelection = () => {
        this.setState({
            selected: null,
            inputVal: ""
        }, () => {
            this.props.onClear ? this.props.onClear() : null
            if(!this.props.name) { return }
            const target = document.querySelector(`input[name="${this.props.name}"]`)
            const event = new Event('change');
            target.dispatchEvent(event);
        })
    }

    selectOptionPk = (pk) => {
        //support multiple later
        const valid_option = this.state.options.filter(opt => opt[0] == pk)
        if(!valid_option.length > 0) {
            return
        }
        const label = valid_option[0][1] 
        this.setState({
            selected: pk,
            inputVal: label
        }, () => {
            this.props.onSelect ? this.props.onSelect(this.state): null
            if(!this.props.name) { return }
            const target = document.querySelector(`input[name="${this.props.name}"]`)
            const event = new Event('change');
            target.dispatchEvent(event);
        })
    }

    selectOption = (evt) => {
        if (this.props.multiple) {
            const new_selection = [...this.state.selection_list]
            new_selection.push([evt.target.dataset.pk, evt.target.textContent])
            this.setState({
                selection_list: new_selection,
                inputVal: ""
            })    
        }else {
            this.setState({
                selected: evt.target.dataset.pk,
                inputVal: evt.target.textContent
            }, () => {
                this.props.onSelect ? this.props.onSelect(this.state): null
                if(!this.props.name) { return }
                const target = document.querySelector(`input[name="${this.props.name}"]`)
                const event = new Event('change');
                target.dispatchEvent(event);
            })
        }
    }

    removeSelection = (evt) => {
        const pk = $(evt.currentTarget).data('id')
        const newSelection = this.state.selection_list.filter(opt => opt[0] != pk)
        this.setState({selection_list: newSelection})
    }

    render() {
        return (
            <div className={styles.container} 
                 id={`${this.props.name 
                            ? this.props.name 
                            : Math.random().toString(36).substring(7)}_widget`}>
                {this.props.name 
                    ? this.props.multiple
                        ? this.state.selection_list.map(opt =>(
                            <input type="hidden" name={this.props.name} value={opt[0]} key={opt[0]} />
                        ))
                        : <input type='hidden' name={this.props.name} value={this.state.selected || ""} />
                    : null }
                <div className={this.props.multiple 
                                    ? styles.selectThreeInput
                                    : ""}>
                    {this.props.multiple 
                        ? <div>
                            {this.state.selection_list.map(s =>(
                                <span className={styles.multipleSelection} key={s[0]}>
                                    <span data-id={s[0]} 
                                        className={styles.multipleSelectionClear}
                                        onClick={this.removeSelection}><i className="fa fa-times" aria-hidden="true"></i></span>
                                    {s[1]}
                                </span>
                            ))}
                        </div>
                        : null}
                    <div>
                        <input 
                            className={this.props.multiple 
                                ? 'form-control form-control-sm ' + styles.multipleInput 
                                :'form-control form-control-sm'} 
                            type='text' 
                            id={`${this.props.name 
                                ? this.props.name 
                                : Math.random().toString(36).substring(7)}_visible_input`}
                            autoComplete="new-password"
                            value={this.state.inputVal}
                            disabled={this.state.disabled} 

                            onChange={this.handleInputChange}
                            onFocus={() => {
                                this.refreshOptions(false)
                                this.setState({showOptions: true})
                            }}
                            style={{
                                backgroundColor: this.state.disabled
                                    ? this.props.clear ? "white" : "#eee" 
                                    : this.props.required 
                                        ? '#bbdfc8'
                                        : 'white',
                                border: this.props.clear
                                    ? "0px"
                                    : null        
                            }}
                            onBlur={() => setTimeout(() =>this.setState({showOptions: false}), 500)} />
                    </div>
                </div>
                <ul className={styles.option_list} 
                    style={{display: this.state.showOptions 
                                        ? "block"
                                        : "none"
                            }}
                    id={`${this.props.name
                        ? this.props.name
                        : randomID()}_widget_options_list`}
                    >
                    {this.state.filteredOptions.map(opt => (
                        <li data-pk={opt[0]} 
                            key={opt[0]} 
                            id={`${this.props.name
                                     ? this.props.name
                                     : randomID()}_widget_opt_${opt[0]}`} 
                            onClick={this.selectOption}>
                                {opt[1]}
                        </li>
                    ))}
                </ul>
            </div>
        )
    }
}

export default Radium(SelectThree)