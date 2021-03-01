import Axios from 'axios';

export default function getHostMeetings(){
    return [[{
        eventName:"Event 1",
        eventTime:" 20/02/21 : 1600",
        tag:"Tag1"
    }, 
    {
        eventName:"Event 2",
        eventTime:" 26/02/21 : 1300",
        tag:"Tag1"
    }, 
    {
        eventName:"Event 3",
        eventTime:" 11/03/21 : 2200",
        tag:"Tag3"
    }], ["Tag1", "Tag3"]]
}