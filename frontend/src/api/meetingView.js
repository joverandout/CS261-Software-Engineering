import API from "../backendApi";

export default async function meetingView(data){
    console.log(data)
    return API.post("/meetingview",data).then(res => {
        console.log(res)
        return res
    }).catch(err => {
        
        throw new Error("Could not send pdf")
    })
}
