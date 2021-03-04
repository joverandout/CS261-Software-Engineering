import API from "../backendApi";

export default async function stopMeeting(data){
    return API.post("/stopmeeting", data).then(res=>{
        console.log(res)
        return true
    }).catch(err=>{
        throw new Error("could not stop the meeting")
    })
}

