import API from "../backendApi";

export default async function meetingCreation(data){
    return API.post("/meetingcreation", data).then(res=>{
        return true
    }).catch(err=>{
        throw new Error("could not create the meeting")
    })
}
