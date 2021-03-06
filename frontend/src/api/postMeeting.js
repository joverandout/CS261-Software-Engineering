import API from "../backendApi";

export default async function postMeetingFeedback(data){

    return API.post("/postmeetingfeed",data).then(res => {
        return true
    }).catch(err => {
        throw new Error("Could not send feedback")
    })
}
