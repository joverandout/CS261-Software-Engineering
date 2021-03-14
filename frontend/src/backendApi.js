import Axios from "axios"
//set the base url in one place, useful when the server is deployed
export default Axios.create({
    baseURL: "http://127.0.0.1:5000"
});