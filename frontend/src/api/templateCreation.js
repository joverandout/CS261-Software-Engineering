import API from "../backendApi";

export default async function templateCreation(data){
    return API.post("/newtemplate", data).then(res=>{
        return true
    }).catch(err=>{
        throw new Error("Could not create template")
    })
}

