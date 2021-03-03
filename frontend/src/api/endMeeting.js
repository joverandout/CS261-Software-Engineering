import API from "../backendApi";

export default async function(data){
    API.post("/endmeeting", data).then(res=>{
        return true
    }).catch(err=>{
        return false
    })
}

