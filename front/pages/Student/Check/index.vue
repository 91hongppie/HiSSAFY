<template>
  <div class="container" onunload="videoOff()">
    <header>
      <h1 class="titles text-center mb-5">
        체크하기
      </h1>
      <div class="text-center">
        <p id="ClockDisplay" class="clock" onload="showTime()" />
      </div>
    </header>
    <div class="screens text-center">
      <p class="describe text-center">얼굴을 중앙에 두고 터치합니다.</p>
    </div>
    <div class="chk-face text-center">
      <div id="btns" style="visibility: hidden; margin-top: 50px;">
        <p class="describe text-center mt-5">사진 확인</p>
        <img src="">
        <v-btn id="yes" to="/student/check/completed_check" color="success mr-5" large>확인</v-btn>
        <v-btn id="no" color="deep-orange ml-5" large @click="refresh()">다시 찍기</v-btn>
      </div>
      <img class="mt-5" src="">
    </div>
    <video id="face-video" width="720" height="560" autoplay muted />
  </div>
</template>

<script>
import * as faceapi from 'face-api.js'

export default {
  mounted () {
    this.start()
    // this.getVideo()
  },
  beforeLeave (to, from, next) {
    this.videoOff()
    next()
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
    start () {
      return Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
        faceapi.nets.faceExpressionNet.loadFromUri('/models')
      ]).then(this.initFace())
    },
    initFace () {
      const video = document.getElementById('face-video')
      navigator.mediaDevices.getUserMedia({ video: {} })
        .then(function (stream) {
          video.srcObject = stream
        })
        .catch(err => console.error(err))

      video.addEventListener('play', () => {
        const canvas = faceapi.createCanvasFromMedia(video)
        // document.body.append(canvas)
        const displaySize = {
          width: video.width,
          height: video.height
        }
        faceapi.matchDimensions(canvas, displaySize)
        setInterval(async () => {
          const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            // .withFaceLandmarks()
            // .withFaceExpressions()
          // const resizedDetections = faceapi.resizeResults(detections, displaySize)
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
          // faceapi.draw.drawDetections(canvas, resizedDetections)
          if (detections) {
            const ctx = canvas.getContext('2d')
            for (const detectIndex in detections) {
              ctx.drawImage(video, detections[`${detectIndex}`]._box.x, detections[`${detectIndex}`]._box.y, detections[`${detectIndex}`]._box.width, detections[`${detectIndex}`]._box.height, detections[`${detectIndex}`]._box.x, detections[`${detectIndex}`]._box.y, detections[`${detectIndex}`]._box.width, detections[`${detectIndex}`]._box.height)
            }
            const imageURI = canvas.toDataURL('image/jpeg')
            const blob = this.dataURItoBlob(imageURI)
            const formdata = new FormData()
            formdata.append('pic_name', blob)
            return this.$axios.$post('/api/recognition/', formdata)
              .then(function (data) {
                console.log(data)
              })
              .catch(e => console.error(e))
            // detections.forEach(function (detection) {
            //   const canvas1 = document.getElementById('canvas1')
            //   const ctx = canvas1.getContext('2d')
            //   const img = new Image()
            //   img.src = video
            //   img.onload = function () {
            //     ctx.drawImage(img, detection._box.x, detection._box.y, detection._box.width, detection._box.height)
            //   }
            //   console.log(typeof img)
            //   console.log(img)
            // })
          }
        }, 500)
      })
    },
    // getVideo () {
    //   const constraints = { audio: false, video: true }
    //   const video = document.querySelector('video')
    //   const canvas = document.querySelector('canvas')
    //   const context = canvas.getContext('2d')
    //   let localMediaStream = null

    //   function snapshot () {
    //     if (localMediaStream) {
    //       const image = document.querySelector('img')
    //       context.drawImage(video, 0, 0, 640, 480)
    //       image.src = canvas.toDataURL('image/png')
    //     }
    //   }
    //   video.addEventListener('click', snapshot, false)

    //   navigator.mediaDevices.getUserMedia(constraints)
    //     .then(function (stream) {
    //       // Older browsers may not have srcObject
    //       if ('srcObject' in video) {
    //         video.srcObject = stream
    //         localMediaStream = stream
    //       } else {
    //         // Avoid using this in new browsers, as it is going away.
    //         video.src = window.URL.createObjectURL(stream)
    //         localMediaStream = stream
    //       }
    //       video.onloadedmetadata = function (e) {
    //         video.play()
    //       }
    //       function chkPath () {
    //         if (window.location.pathname !== '/student/check') {
    //           video.pause()
    //           video.src = ''
    //           localMediaStream.getTracks()[0].stop()
    //         }
    //       }
    //       const btn = document.querySelector('#yes')
    //       btn.addEventListener('click', chkPath)
    //     })
    //     .catch(function (err) {
    //       alert(err.name + ': ' + err.message)
    //     })
    // },
    videoOff () {
      const monitor = document.querySelector('video')
      monitor.pause()
      monitor.src = ''
      // localstream.getTracks()[0].stop()
      alert('Video off')
    },
    showTime () {
      const date = new Date()
      let h = date.getHours() // 0 - 23
      let m = date.getMinutes() // 0 - 59
      let s = date.getSeconds() // 0 - 59
      let session = 'AM'

      if (h === 0) {
        h = 12
      }

      if (h > 12) {
        h = h - 12
        session = 'PM'
      }

      h = (h < 10) ? '0' + h : h
      m = (m < 10) ? '0' + m : m
      s = (s < 10) ? '0' + s : s

      const time = h + ':' + m + ':' + s + ' ' + session
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
    refresh () {
      window.location.reload()
    }
  }
}
</script>

<style scoped>
.titles {
  font-size: 100pt;
  color: #ffffff;
}

.clock {
  position: relative;
  color: #706c61;
  font-size: 65pt;
  font-family: 'Helvetica';
  /* letter-spacing: 3px; */
}

.describe{
  font-size: 60pt;
  color: #ffffff;
}

#face-video {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

canvas {
  display: None;
}

</style>
