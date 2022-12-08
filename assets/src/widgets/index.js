import React from 'react';
import ReactDOM from 'react-dom/client'
import OneTable from './awesome_table/container/root';
import axios from 'axios';
import BaseTreeSelectWidget from './treeview';
import { node } from 'prop-types';
import SelectThree from '../select_3'

const children = document.querySelectorAll('.child-table')

children.forEach((el, idx) => {
    const app = el.dataset.app
    const model = el.dataset.model
    const root = ReactDOM.createRoot(el)
    const isUpdate = location.href.split('/').includes('update')
    axios({
        method: "GET",
        url: `/api/child-table-properties/${app}/${model}/`
    }).then(res => {
        root.render(
            <OneTable
              model_id={`${app}.${model}`}
              inputID={`id_${model}`}
              fields={res.data.properties}
              readOnly={isUpdate && res.data.update_read_only}
              tabIndex={idx}
            />)
    })
})


const tree = document.getElementById('tree')

if(tree && tree.dataset.url) {
    axios({
        method:"GET",
        url: tree.dataset.url
    }).then(res => {
        const root = ReactDOM.createRoot(tree)
        root.render(
            <BaseTreeSelectWidget 
                data={res.data.data}
                branchClick={(node, branch) => {console.log("Do something!")}}
                leafClick={(node) => {console.log("Do something!")}}
                dataMapper={node => node}
            />)    
    })
    
}


const search = document.querySelectorAll('.search-widget')


search.forEach(field => {
    const multiple = field.classList.contains('multiple')
    let selected = ''
    
    if(multiple) {
        selected = Array.from(field.options).filter(opt => opt.selected).map(opt => opt.value)
    }else {
        selected = field.value
    }
    const root = ReactDOM.createRoot(field.parentElement)
    root.render(<SelectThree 
        filters={field.dataset.filters || ""}
        model={field.dataset.model}
        initial={selected}
        app={field.dataset.app}
        required={field.required}
        multiple={multiple}
        disabled={field.disabled || Array.from(field.classList).includes("read-only")}
        name={field.name}/>)
})