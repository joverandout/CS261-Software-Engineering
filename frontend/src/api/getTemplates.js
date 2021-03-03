import API from "../backendApi";

export default async function getTemplates(data){
    return API.post("/gettemplates", data).then(res=>{
        return res.data
    }).catch(err=>{
        
         throw new Error("could not get templates")
    })
}
