import API from "../backendApi";

export default async function getHostMeetings(data){
    
    return API.post("/hostmain", data).then(res=>{
        let categories = []
        res.array.forEach(event => {
            categories.push (event.Category)
        });
        return [res, categories]
    }).catch(err=>{
        throw new Error("Could not retrieve host's events")
    })

    

}