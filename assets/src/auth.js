/* Copyright (c) 2021,  C.Kandoro and Contributors.
 * See Licence for more details.
 */

import 'regenerator-runtime/runtime'
import axios from 'axios'


const authAxiosInstance = axios.create({})


authAxiosInstance.interceptors.request.use(async config =>{
    let token = 'Token ' 
    
    // TODO reduce requests using local storage cache and cache invalidation
    const resp = await (await axios.get('/api/user-token/')).data.token
    config.headers.Authorization = token + resp
    return config
})

authAxiosInstance.defaults.xsrfCookieName = "csrftoken";
authAxiosInstance.defaults.xsrfHeaderName = "X-CSRFTOKEN";


export default authAxiosInstance