<template>
  <div class="container blue" onunload="videoOff()">
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
      <video autoplay="true" @click="hideShow()">No video support in your browser</video>
    </div>
    <div class="chk-face text-center">
      <div id="btns" style="visibility: hidden; margin-top: 50px;">
        <p class="describe text-center mt-5">사진 확인</p>
        <img src="">
        <canvas style="display:none;" width="640" height="480" />
        <p></p>
        <v-btn id="yes" to="/student/check/completed_check" color="success mr-5" large>확인</v-btn>
        <v-btn id="no" color="deep-orange ml-5" large @click="refresh()">다시 찍기</v-btn>
      </div>
      <img class="mt-5" src="">
      <canvas style="display:none;" width="640" height="480" />
    </div>
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
    start () {
      const uri = '/assets/models'
      Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(uri),
        faceapi.nets.faceLandmark68Net.loadFromUri(uri),
        faceapi.nets.faceRecognitionNet.loadFromUri(uri),
        faceapi.nets.faceExpressionNet.loadFromUri(uri)
      ]).then(this.startVideo())
    },
    startVideo () {
      const video = document.querySelector('video')
      navigator.mediaDevices.getUserMedia({ audio: false, video: true })
        .then(function (stream) {
          video.srcObject = stream
        })
        .catch(err => console.error(err))

      video.addEventListener('play', () => {
        const canvas = faceapi.createCanvasFromMedia(video)
        document.body.append(canvas)
        const displaySize = { width: video.width, height: video.height }
        faceapi.matchDimensions(canvas, displaySize)
        setInterval(async () => {
          const detections = await faceapi.detectAllFaces(video,
            new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceExpressions()
          const resizedDetections = faceapi.resizeResults(detections, displaySize)
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
          faceapi.draw.drawDetections(canvas, resizedDetections)
          faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
          faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
        }, 100)
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
</style>
