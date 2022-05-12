const getHook = (tabIndex, hookname) => {
    return undefined
    let hooks
    if(window.rform) {
        hooks = window.rform._hooks[tabIndex]
    } else {
        hooks = form._hooks[tabIndex]
    }
    if(!hooks) {
        return undefined
    }
    return hooks[hookname]
    
}

export default getHook