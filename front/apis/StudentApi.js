import axios from 'axios'

const Enroll = (data, callback, errorCallback) => {
  axios.post('https://i02b106.p.ssafy.io/api/add/account/', data)
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
