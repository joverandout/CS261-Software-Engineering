import API from "../backendApi";

export default async function startMeeting(data){
    return API.post("/startmeeting", data).then(res=>{
        
        return res.data
    }).catch(err=>{
        throw new Error("could not start the meeting")
    })
}

