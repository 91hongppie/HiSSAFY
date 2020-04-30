<template>
  <div class="container blue">
    <v-dialog />
    <div id="goback">
      <v-btn color="secondary mr-5" @click="goBack()">뒤로가기</v-btn>
    </div>
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
      </div>
      <div class="video">
        <video id="face-video" autoplay="true" @click="hideShow()">No video support in your browser</video>
      </div>
      <div class="chk-face">
        <div id="btns" style="visibility: hidden; margin-top: 50px;">
          <p class="describe text-center mt-5">사진 확인</p>
          <img src="">
          <canvas style="display:none;" width="640" height="480" />
          <p />
          <v-btn id="yes" color="success mr-5" large :disabled="!isSubmit" @click="stopSave()">제출</v-btn>
          <v-btn id="no" color="deep-orange ml-5" large @click="videoShow()">다시 찍기</v-btn>
          <div class="infos">
            <v-text-field v-model="form.name" label="이름" placeholder="예: 홍길동" />
            <v-text-field
              v-model="form.student_id"
              label="학번"
              placeholder="예: 0123567"
              :rules="[rules.studentIdConfirm(form.student_id)]"/>
            <v-select
              v-model="form.campus"
              :items="items"
              label="캠퍼스"
              :rules="[rules.campusConfirm(form.campus)]"/>
            <v-text-field
              v-model="form.stage"
              label="기수"
              placeholder="2기인 경우: 2 입력"
              :rules="[rules.infoConfirm(form.stage)]"/>
            <v-text-field
              v-model="form.classes"
              label="반"
              placeholder="1반인 경우: 1 입력"
              :rules="[rules.infoConfirm(form.classes)]"/>
            <v-text-field
              v-model="form.birthday"
              label="생일"
              placeholder="예: 1990-01-01"
              :rules="[rules.birthdayConfirm(form.birthday)]"/>
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
      form: {
        name: '',
        student_id: '',
        stage: '',
        classes: '',
        birthday: '',
        campus: ''
      },
      items: ['서울', '대전', '구미', '광주'],
      isSubmit: false,
      rules: {
        studentIdConfirm: v => (v.length === 7 && !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-z|A-Z]/.test(v)) || '7자리의 숫자를 입력해야합니다.',
        infoConfirm: v => (!/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-z|A-Z]/.test(v)) || '숫자만 입력해주세요.',
        birthdayConfirm: v => (v.length === 10 &&
        !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-z|A-Z]/.test(v.slice(0, 4)) &&
        !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-z|A-Z]/.test(v.slice(5, 7)) &&
        v.slice(5, 7) <= 12 &&
        !/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣|a-z|A-Z]/.test(v.slice(8, 10)) &&
        v.slice(8, 10) <= (new Date(v.slice(0, 4), v.slice(5, 7), 0)).getDate()) ||
       '생일을 올바르게 입력해주세요.',
        campusConfirm: v => (v.length === 2) || '캠퍼스를 선택해주세요.'
      }
    }
  },
  watch: {
    form: {
      deep: true,
      handler () {
        const checkform = this.checkForm()
        if (checkform) {
          this.isSubmit = true
        } else {
          this.isSubmit = false
        }
      }
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
    goBack () {
      this.$router.push('/')
    },
    checkForm () {
      if (this.rules.campusConfirm(this.form.campus) === true &&
        this.rules.studentIdConfirm(this.form.student_id) === true &&
        this.rules.infoConfirm(this.form.stage) === true &&
        this.rules.infoConfirm(this.form.classes) === true &&
        this.rules.birthdayConfirm(this.form.birthday) === true) {
        this.isSubmit = true
        return true
      } else {
        this.isSubmit = false
        return false
      }
    },
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
      const yes = document.getElementById('yes')
      if (btns.style.visibility === 'hidden') {
        btns.style.visibility = 'visible'
      }
      yes.style.visibility = 'visible'
    },
    videoShow () {
      const image = document.querySelector('img')
      const yes = document.getElementById('yes')
      image.src = ''
      // if (yes.style.visibility === 'visible') {
      yes.style.visibility = 'hidden'
      // }
    },
    stopSave () {
      const canvas = document.querySelector('canvas')
      const image = document.querySelector('img')
      image.src = canvas.toDataURL('image/png')
      const blob = this.dataURItoBlob(image.src)
      const formdata = new FormData()
      formdata.append('pic_name', blob)
      formdata.append('name', this.form.name)
      formdata.append('student_id', this.form.student_id)
      formdata.append('stage', this.form.stage)
      formdata.append('classes', this.form.classes)
      formdata.append('birthday', this.form.birthday)
      formdata.append('region', this.form.campus)
      StudentApi.Enroll(
        formdata,
        (res) => {
          if (res.status === 200) {
            document.querySelector('video').pause()
            this.$router.push({
              path: '/student/enroll/completed_enroll'
            })
          } else if (res.status === 204) {
            this.$modal.show('dialog', {
              text: '얼굴이 잘나오도록 사진을 다시 촬영해주세요.'
            })
          }
        },
        () => {
          this.$modal.show('dialog', {
            text: '개인정보를 다시 한번 확인해주세요.'
          })
        }
      )
    }
  }
}
</script>

<style scoped>
#goback {
  margin-top: 30px;
  margin-bottom: 30px;
}

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

.example-modal-content {
  height: 100%;
  box-sizing: border-box;
  padding: 10px;
  font-size: 13px;
  overflow: auto;
}

.video {
  display: flex;
  width: 100%;
  justify-content: center;
}

#face-video {
  width: 50%;
  height: 50%;
}

#goback {
  display: flex;
  width: 100%;
  align-content: center;
  justify-content: center;
}
</style>
