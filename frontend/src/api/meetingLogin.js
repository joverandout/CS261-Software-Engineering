import API from "../backendApi";

export default async function meetingLogin(data){

    return API.post("/login",data).then(res => {
        return res.data
    }).catch(err => {
        throw new Error("Could not log in")
    })
}
