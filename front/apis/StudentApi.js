import axios from 'axios'

const Enroll = (data, callback, errorCallback) => {
  const form = new FormData()
  form.append(data)

  axios.post('http://127.0.0.1/api/account/', form)
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
