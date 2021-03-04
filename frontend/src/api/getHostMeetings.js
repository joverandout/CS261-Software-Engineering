import API from "../backendApi";

export default async function getHostMeetings(data){
    
    return API.post("/hostmain", data).then(res=>{
        let categories = []
        res.data.forEach(event => {
            categories.push (event.Category)
        });
        return [res.data, categories]
    }).catch(err=>{
        console.log(err.message)
        throw new Error("Could not retrieve host's events")
    })

    

}