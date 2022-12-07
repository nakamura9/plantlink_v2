const workOrderScript = () => {
    form.onChange('machine', () => {
        form.section_widget.setState({
            filters: {machine: form.getVal('machine')}
        })
    })

    form.onChange('section', () => {
        form.subunit_widget.setState({
            filters: {section: form.getVal('section')}
        })
    })

    form.onChange('subunit', () => {
        form.subassembly_widget.setState({
            filters: {subunit: form.getVal('subunit')}
        })
    })

    form.onChange('subassembly', () => {
        form.component_widget.setState({
            filters: {subassembly: form.getVal('subassembly')}
        })
    })

    console.log('run')

}

$(document).ready(() => {
    switch(location.pathname) {
        case '/create/maintenance/workorder/':
        case '/update/maintenance/workorder/':
        case '/create/maintenance/checklist/':
        case '/update/maintenance/checklist/':
        case '/create/maintenance/preventativetask/':
        case '/update/maintenance/preventativetask/':
            setTimeout(workOrderScript, 1000)
            break
        default:
            console.log("Scripts loaded")
    }
})