import API from "../backendApi";

export default async function meetingView(data){

    return API.post("/meetingView",data).then(res => {
        console.log(res)
        return res
    }).catch(err => {
        throw new Error("Could not send feedback")
    })
}
