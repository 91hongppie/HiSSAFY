import axios from 'axios'

const Enroll = (data, callback, errorCallback) => {
  console.log(data)
  axios.post('http://127.0.0.1:8000/api/add/account/', data)
    .then((res) => {
      callback(res)
    })
    .catch((err) => {
      errorCallback(err)
    })
}

const StudentApi = {
  Enroll: (data, callback, errorCallback) => Enroll(data, callback, errorCallback)
}

export default StudentApi
