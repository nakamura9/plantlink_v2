import React from 'react'
import styles from './table.css'

const Header = (props) => {
    return (
        <thead>
            <tr className={styles.header}>
                <th style={{width: '60px'}}></th>
                {props.fields.filter(f => !f.hidden).map(field => (
                    <th 
                      key={field.name} 
                      style={{
                                width: field.width ? `${field.width}%` : "auto",
                                textAlign: ['number', 'int'].indexOf(field.type) > -1 ? "right" : "left"
                            }}>
                          {field.label}
                    </th>)
                )}
            </tr>
        </thead>
    )
}

export default Header;