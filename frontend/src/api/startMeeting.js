import API from "../backendApi";

export default async function startMeeting(data){
    return API.post("/startmeeting", data).then(res=>{
        return true
    }).catch(err=>{
        throw new Error("could not start the meeting")
    })
}

