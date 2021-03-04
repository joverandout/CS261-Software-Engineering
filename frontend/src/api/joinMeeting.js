import API from "../backendApi";

export default function joinMeeting(data){
    return API.post("/meetinglogin",data).then(res=>{
        let template ={
            emotions:res.data.emotionsselected,
            questions:res.data.questions
        }
        return{
            meetingid:res.data.meetingid,
            companyid:res.data.companyid,
            template:template
        }
    }).catch(err=>{
        throw err
    })
}