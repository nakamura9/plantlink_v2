import React from 'react'
import {useState, useEffect} from 'react'
import axios from 'axios'
// import {Link} from "react-router-dom"

const renderData = (field, value, rowData) => {
    let renderedData
    switch(field.type) {
        case 'number':
            renderedData = !([null, undefined].includes(value) || isNaN(value)) ? parseFloat(value).toFixed(2) : ""
            break;
        case 'int':
            renderedData = !([null, undefined].includes(value) || isNaN(value))  ? parseInt(value) : ""
            break;
        case 'link':
            console.log(rowData)
            const id = rowData[field.name + "_id"]
            const [app, model] = field.options.split('.')
            renderedData = <a href={`/update/${app}/${model}/${id}`} target="_blank">{value}</a>
            break;
        case 'text':
        case 'char':
        case 'time':
        case 'date':
            renderedData = value
            break;
        case 'select': 
            if(field.options && value != null) {
                const matchingOption = field.options.filter(opt => opt[0] == value)
                renderedData = matchingOption && matchingOption[0] ? matchingOption[0][1] : value
            } else {
                renderedData = value
            }
            break;
        case 'bool': 
            renderedData = <div style={{display:'flex', justifyContent: 'center'}}>
                {value == 'on' || value === true
                    ? <i className="fa fa-check" aria-hidden="true"></i>
                    : <i className="fa fa-times" aria-hidden="true"></i>}
            </div>
            break;
        case 'dynamic_search':
            renderedData =  <DynamicField  {...value} />
        default:
            break;
    }
    return renderedData
}

const DynamicField = (props) => {
    const [model, setModel] = useState("") 
    const [instance, setInstance] = useState("")
    useEffect(() => {
        if(props.model) {
            const [app, modelname] = props.model.split('.')
            axios.get(`/base/api/get-instance-name/${app}/${modelname}/${props.instance}/`)
                .then(res => {
                    setModel(res.data.name)
                    setInstance(res.data.instance)
                })
        }
    }, [])
    const spanStyle = {
        backgroundColor: '#aaa',
        color: 'white',
        fontWeight: 600,
        padding: '0.25rem 0.5rem',
        borderRadius: '0.2rem',
    }
    if(!props.model) {
        return <span></span>
    }
    return (<div>
                <span style={spanStyle}>{model}</span> {instance}
            </div>)
}

export default renderData