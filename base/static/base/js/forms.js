window.form = window.form || {}

Object.assign(window.form, {
    _hooks: [],
    onload(func) {
        $(document).ready(func)
    },
    onChange(field, func) {
        this._getField(field).on('change', (evt) => {
            func(evt.target.value)
        })
    },
    onInput(field, func) {
        this._getField(field).on('input', (evt) => {
            func(evt.target.value)
        })
    },
    _getField(fieldname) {
        if($(`input[name="${fieldname}"]`).length == 1) {
            return $(`input[name="${fieldname}"]`)
        }else if ($(`select[name="${fieldname}"]`).length == 1) {
            return $(`select[name="${fieldname}"]`)
        } else if ($(`textarea[name="${fieldname}"]`).length == 1) {
            return $(`textarea[name="${fieldname}"]`)
        }else {
            return null
        }
    },
    _getContainer(fieldname) {
        return  $(`#div_id_${fieldname}`)
    },
    getVal(fieldname) {
        const field = this._getField(fieldname)
        if(field.attr('type') == "checkbox") {
            return field.is(":checked")
        }

        return field.val()
    },
    setVal(fieldname, value) {
        console.log("Wrong one!")
        if(this.hasOwnProperty(fieldname + "_widget")) {
            if(value == null) {
                this[fieldname + "_widget"].clearSelection()
            }
            this[fieldname + "_widget"].selectOptionPk(parseInt(value))
        }else {
            const element = this._getField(fieldname)
            element.val(value)
            element.trigger('change');
        }
    },
    setTabVal(tabIndex, fieldname, value) {
        if(!tabIndex) {
            tabIndex = 0
        }
        
    },
    disableField(fieldname) {
        if(this.hasOwnProperty(fieldname + "_widget")) {
            this[fieldname + "_widget"].setState({disabled: true})
        }else {
            this._getField(fieldname).prop('disabled', true)
        }
    },
    hideField(fieldname) {
        this._getContainer(fieldname).css('display', 'none')
    },
    showField(fieldname) {
        this._getContainer(fieldname).css('display', 'block')
    },
    formatDate(date){
        const month = date.getMonth() + 1
        const day = date.getDate()
        return `${date.getFullYear()}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`
    },
    readOnlyField(fieldname) {
        if(this.hasOwnProperty(fieldname + "_widget")) {
            this[fieldname + "_widget"].setState({disabled: true})
        }else {
            const field = this._getField(fieldname)
            if(field[0].nodeName == "SELECT") {
                field.css('pointer-events', 'none')
                field.css('background-color', '#eee')
            }
            field.prop('readonly', true)
        }
    },
    self() {
        return $('form')
    },
    currentUser() {
        return $('input[name="session_user"]').val()
    },
    currentEmployee() {
        return $('input[name="session_employee"]').val()
    },
    setTitle(newTitle) {
        $('#title-text > span').text(newTitle)
    },
    setHook(idx, obj) {
        if(idx > 0 && this._hooks.length - 1 < idx) {
            console.warn('Index of hook is greater than hook array length')
            this._hooks.push(obj)
        } else {
            this._hooks[idx] = obj
        }
    }
})

$(document).ready(() => {
    // $('input[type="number"]').on('change', (evt) => {
    //     $(evt.target).val(parseFloat(evt.target.value).toFixed(2))
    // })
    $.each($('input[data-readonly="true"], select[data-readonly="true"], textarea[data-readonly="true"] '), function(idx, el) {
        form.readOnlyField(el.name)
    })
})

window.money = (val) => {
    if(!val) {
        return 0.00
    }
    let number = val
    if(typeof(val) == "string") {
        number = parseFloat(val)
    }
    return parseFloat(number.toFixed(2))
}