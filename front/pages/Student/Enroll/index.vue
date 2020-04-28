<template>
  <div class="container blue">
    <header>
      <h1 class="titles text-center mb-5">
        얼굴 등록하기
      </h1>
      <div class="text-center">
        <p id="ClockDisplay" class="clock" />
      </div>
    </header>
    <div class="screens text-center">
      <div class="vid">
        <p class="describe text-center">얼굴을 중앙에 두고 클릭합니다.</p>
        <video autoplay="true" @click="hideShow()">No video support in your browser</video>
      </div>
      <div class="chk-face">
        <div id="btns" style="visibility: hidden; margin-top: 50px;">
          <p class="describe text-center mt-5">사진 확인</p>
          <img src="">
          <canvas style="display:none;" width="640" height="480" />
          <p />
          <v-btn id="yes" color="success mr-5" large @click="stopSave()">제출</v-btn>
          <v-btn id="no" color="deep-orange ml-5" large @click="refresh()">다시 찍기</v-btn>
          <div class="infos">
            <v-text-field v-model="name" label="이름" placeholder="예: 홍길동" />
            <v-text-field v-model="student_id" label="학번" placeholder="예: 0123567" />
            <v-select v-model="campus" :items="items" label="캠퍼스" />
            <v-text-field v-model="stage" label="기수" placeholder="2기인 경우: 2 입력" />
            <v-text-field v-model="classes" label="반" placeholder="1반인 경우: 1 입력" />
            <v-text-field v-model="birthday" label="생일" placeholder="예: 1990-01-01" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StudentApi from '../../../apis/StudentApi'

export default {
  data: () => {
    return {
      pic_name: '',
      name: '',
      student_id: '',
      stage: '',
      classes: '',
      birthday: '',
      items: ['서울', '대전', '구미', '광주'],
      campus: ''
    }
  },
  mounted () {
    this.getVideo()
    this.showTime()
  },
  beforeLeave (to, from, next) {
    document.querySelector('video').pause()
  },
  methods: {
    dataURItoBlob (dataURI) {
      // convert base64/URLEncoded data component to raw binary data held in a string
      let byteString
      if (dataURI.split(',')[0].includes('base64') >= 0) {
        byteString = atob(dataURI.split(',')[1])
      } else {
        byteString = unescape(dataURI.split(',')[1])
      }

      // separate out the mime component
      const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

      // write the bytes of the string to a typed array
      const ia = new Uint8Array(byteString.length)
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }

      return new Blob([ia], { type: mimeString })
    },
    getVideo () {
      const constraints = { audio: false, video: true }
      const video = document.querySelector('video')
      const canvas = document.querySelector('canvas')
      const context = canvas.getContext('2d')
      let localMediaStream = null

      function snapshot () {
        if (localMediaStream) {
          const image = document.querySelector('img')
          context.drawImage(video, 0, 0, 640, 480)
          image.src = canvas.toDataURL('image/jpeg')
        }
      }
      video.addEventListener('click', snapshot, false)

      navigator.mediaDevices.getUserMedia(constraints)
        .then(function (stream) {
          // Older browsers may not have srcObject
          if ('srcObject' in video) {
            video.srcObject = stream
            localMediaStream = stream
          } else {
            // Avoid using this in new browsers, as it is going away.
            video.src = window.URL.createObjectURL(stream)
            localMediaStream = stream
          }
          video.onloadedmetadata = function (e) {
            video.play()
          }
          video.addEventListener('pause', () => {
            const stream = video.srcObject
            const tracks = stream.getTracks()
            tracks.forEach(function (track) {
              track.stop()
            })
            video.srcObject = null
          })
        })
        .catch(function (err) {
          alert(err.name + ': ' + err.message)
        })
    },
    showTime () {
      const date = new Date()
      let h = date.getHours() // 0 - 23
      let m = date.getMinutes() // 0 - 59
      let s = date.getSeconds() // 0 - 59

      h = (h < 10) ? '0' + h : h
      m = (m < 10) ? '0' + m : m
      s = (s < 10) ? '0' + s : s

      const time = h + ':' + m + ':' + s
      document.getElementById('ClockDisplay').textContent = time

      setTimeout(this.showTime, 1000)
    },
    hideShow () {
      const btns = document.getElementById('btns')
      const video = document.querySelector('video')
      if (btns.style.visibility === 'hidden') {
        btns.style.visibility = 'visible'
      } else {
        btns.style.visibility = 'hidden'
      }
      if (video.style.visibility === 'hidden') {
        video.style.visibility = 'visible'
      } else {
        video.style.visbiility = 'hidden'
      }
    },
    stopSave () {
      const canvas = document.querySelector('canvas')
      const image = document.querySelector('img')
      image.src = canvas.toDataURL('image/png')
      const blob = this.dataURItoBlob(image.src)
      const formdata = new FormData()
      formdata.append('pic_name', blob)
      formdata.append('name', this.name)
      formdata.append('student_id', this.student_id)
      formdata.append('stage', this.stage)
      formdata.append('classes', this.classes)
      formdata.append('birthday', this.birthday)
      formdata.append('region', this.campus)
      StudentApi.Enroll(
        formdata,
        (res) => {
          if (res.status === 200) {
            this.$router.push({
              path: '/student/enroll/completed_enroll'
            })
          }
        }
      )
    },
    refresh () {
      window.location.reload()
    }
  }
}
</script>

<style scoped>
.titles {
  font-size: 40pt;
  color: #ffffff;
}

.clock {
  position: relative;
  color: #ffffff;
  font-size: 35pt;
  font-family: 'Helvetica';
  /* letter-spacing: 3px; */
}

.describe {
  font-size: 30pt;
  color: #ffffff;
}
</style>
