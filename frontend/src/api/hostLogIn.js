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

    return API.post("/hostlogin",data).then(res => {
        return res.data.hostid
    }).catch(err => {
        throw new Error("Could not log in")
    })
}
