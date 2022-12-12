import React from 'react' 
import styles from './filters.css'
import renderField from '../../widgets/awesome_table/fields/render'


const Filters = props => {
    return (
        <div className={styles.container} style={{display: props.show ? 'flex': 'none'}}>
            <div>
                <h4>Filter Events</h4>
                <hr />
                {props.fields.map(f => (
                    <div>
                        <label>{f.label}</label>
                        {renderField(f, (props.values[f.name] || null), props.handler, 'form')}
                    </div>
                ))}
                <button 
                    className={'btn btn-primary'}
                    onClick={props.onFilter}
                >Filter</button>
            </div>
        </div>
    )
}

export default Filters