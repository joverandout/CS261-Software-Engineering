import API from "../backendApi";

export default function joinMeeting(data){
    return API.post("/meetinglogin",data).then(res=>{
        let info = res.data[0]
        console.log(info)
        let template ={
            emotions:info.emotionsselected,
            questions:info.questions
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