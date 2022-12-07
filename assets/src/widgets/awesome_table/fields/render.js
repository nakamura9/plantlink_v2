import React from 'react'
import {NumberField, IntegerField} from './number'
import {TextField, CharField} from './text'
// import {DynamicSearchField, SearchField} from './search'
import DateField  from './datetime'
import SelectField from './select'
import BooleanField from './boolean'
import { SearchField } from './search'


const renderField = (field, initial, handler, context) => {
    let renderedField
    switch(field.type) {
        case 'number':
            renderedField = <NumberField 
                              value={initial}
                              name={field.name} 
                              frozen={field.frozen}
                              onChange={handler}
                              />
            break;
        case 'int':
            renderedField = <IntegerField 
                                value={initial}
                                name={field.name} 
                                frozen={field.frozen}
                                onChange={handler}
                                />
            break;
        case 'text':
            renderedField = <TextField 
                              context={context}
                              value={initial}
                              name={field.name} 
                              onChange={handler}
                              frozen={field.frozen}/>
            break;
        case 'char':
            renderedField = <CharField 
                                value={initial}
                                name={field.name} 
                                onChange={handler}
                                frozen={field.frozen}/>
            break;
        case 'link':
            renderedField = <SearchField 
                                options={field.options}
                                name={field.name} 
                                onChange={handler}
                                value={initial}
                                frozen={field.frozen}/>
            break;
        // case 'dynamic_search':
        //     renderedField = <DynamicSearchField 
        //                         options={field.options}
        //                         name={field.name} 
        //                         onChange={handler}
        //                         value={initial}
        //                         frozen={field.frozen}/>
        //     break;
        case 'date':
            renderedField = <DateField 
                                value={initial}
                                name={field.name} 
                                onChange={handler}
                                frozen={field.frozen}/>
            break;
        case 'select': 
            renderedField = <SelectField 
                              value={initial}
                              name={field.name}
                              onChange={handler} 
                              options={field.options}
                              frozen={field.frozen}/>
            break;
        // case 'time': 
        //     renderedField = <TimeField 
        //                       value={initial}
        //                       name={field.name}
        //                       onChange={handler} 
        //                       frozen={field.frozen}/>
        //     break;
        case 'bool': 
            renderedField = <BooleanField 
                                value={initial}
                                name={field.name}
                                onChange={handler} 
                                frozen={field.frozen}/>
            break;
        default:
            break;
    }
    return renderedField
}


export default renderField