import React from 'react'
import SelectThree from '../../select_3'
import DynamicSelect from '../../dynamic_select'
import {useState} from 'react'

const SearchField = (props) => {
    const onSelect = (state) => {
        props.onChange({
            target: {
                name: props.name,
                value: state.inputVal,
                valueID: state.selected 

            }
        })
    }

    const onClear = (evt) => {
        return null
    }
    return  <SelectThree 
                model={props.options.model}
                app={props.options.app}
                filters={props.options.filters}
                name={props.name}
                onSelect={onSelect}
                onClear={onClear}
                initial={props.value}
                disabled={props.frozen}
                clear />
}

const DynamicSearchField = (props) => {
    const onSelect = (state) => {

        props.onChange({
            dynamicField: true,
            model: state.model.name,
            instance: state.instance[0],
            modelname: props.options.modelname,
            instancename: props.options.instancename,
            fieldname: props.name,
            field: {
                model: state.model.name,
                instance: state.instance[0]
            }
        })
    }

    const onClear = () => {
        return null
    }
    return  <DynamicSelect 
                models={props.options.models}
                model_fieldname={props.options.modelname}
                instance_fieldname={props.options.instancename}
                onSelect={onSelect}
                onClear={onClear}
                initial={props.value}
                disabled={props.frozen}
                name={props.name}
            />
}

export {DynamicSearchField, SearchField}
