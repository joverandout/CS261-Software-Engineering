import API from "../backendApi"

/**
 * 
 * @param {*} data 
 * {
 *      username
 *      password
 * }
 * returns
 * {
 *  hostid
 * }
 * or error
 */
export default async function hostLogIn(data){

    return API.post("http://127.0.0.1:5000/login",data).then(res => {
        return res.data.hostid
    }).catch(err => {
        throw new Error("Could not log in")
    })
}
