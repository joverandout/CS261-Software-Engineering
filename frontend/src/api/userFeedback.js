import API from "../backendApi";

export default async function userFeedback(data){

    return API.post("/userfeedback",data).then(res => {
        return true
    }).catch(err => {
        throw new Error("Could not send feedback")
    })
}
