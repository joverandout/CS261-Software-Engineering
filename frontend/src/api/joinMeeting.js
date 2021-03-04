import API from "../backendApi";

export default function joinMeeting(data){
    return API.post("/meetinglogin",data).then(res=>{
        let info = res.data[0]
        
        let template ={
            emotions:info.emotionsselected,
            questions:info.question,
            name:info.templatename
        }
        return{
            meetingid:info.meetingid,
            companyid:info.companyid,
            template:template
        }
    }).catch(err=>{
        throw err
    })
}