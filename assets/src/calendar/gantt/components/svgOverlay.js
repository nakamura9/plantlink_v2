import React, {useEffect, useState} from 'react'
import styles from '../style.css'

const svgOverlay  = (props) => {
    const [lines, setLines]  = useState([])
    useEffect(()=> {
        const tasksWithIndicies = props.tasks.map((t, index) => ({...t, index:index}))
        const filteredTasks = tasksWithIndicies.filter(t => t.next != null && new Date(t.date).getMonth() == new Date(t.next).getMonth() )
        setLines(filteredTasks.map(task => {
            const topOffset = 72 + 16
            const marginBottom = 12
            const barHeight = 36
            const dayWidth = 48
            const startDate = new Date(task.date)
            const nextDate = new Date(task.next)
            const startX = dayWidth * (startDate.getDate() + task.span)
            const startY = topOffset + ((barHeight + marginBottom) * task.index)
            
            const endX  = dayWidth * (nextDate.getDate() - 1)
            const endY = topOffset + ((barHeight + marginBottom) * (task.index + 1)) // naive, tasks can be in varying sequences
            const start = [startX, startY]
            const end = [endX, endY]
            
            const points = [start,  [startX + 20, startY]]
            if(startX + 40 > endX) {
                const midpoint = startY + ((endY - startY) / 2)
                points.push([startX + 20, midpoint])
                points.push([endX - 20, midpoint])
                points.push([endX - 20, endY])
            } else {
                points.push([startX + 20, endY])
            }
            
            points.push(end)

            const cap = [[endX - 8, endY - 8], end, [endX - 8, endY + 8]]


            return {
                points: points.map(p => `${p[0]},${p[1]}`).join(" "),
                cap: cap.map(p => `${p[0]},${p[1]}`).join(" ")
            }
        }))

    }, [props.tasks])

    const lineStyle = {
        fill:'none',
        stroke:"#aaa",
        strokeWidth:1.5
    }

    return  <svg width={props.width} height={props.height} className={styles.overlay}>
        {lines.map((line, i) => (
            <g key={i}>
                <polyline
                    points={line.points} 
                    style={lineStyle}
                />
                <polyline 
                    points={line.cap}
                    style={lineStyle}
                />
            </g>
        ))}
    </svg>
}

export default svgOverlay