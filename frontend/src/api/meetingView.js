import API from "../backendApi";

export default async function meetingView(data){
    
    return API.post("/meetingview",data).then(res => {
        
        return res.data
    }).catch(err => {
        
        throw new Error("Could not send pdf")
    })
}
