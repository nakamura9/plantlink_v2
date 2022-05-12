import React from 'react';
import ReactDOM from 'react-dom/client'
import OneTable from './awesome_table/container/root';
import axios from 'axios';
import BaseTreeSelectWidget from './treeview';
import { node } from 'prop-types';

const children = document.querySelectorAll('.child-table')

children.forEach((el, idx) => {
    const app = el.dataset.app
    const model = el.dataset.model
    const root = ReactDOM.createRoot(el)
    axios({
        method: "GET",
        url: `/api/child-table-properties/${app}/${model}/`
    }).then(res => {
        console.log(res.data)
        root.render(
            <OneTable
              model_id={`${app}.${model}`}
              inputID={`id_${model}`}
              fields={res.data.properties}
              tabIndex={idx}
            />)
    })
})


const tree = document.getElementById('tree')

if(tree && tree.dataset.url) {
    console.log(tree.dataset.url)
    axios({
        method:"GET",
        url: tree.dataset.url
    }).then(res => {
        console.log(res.data.data)
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