<template>
  <div class="container" onunload="videoOff()">
    <header>
      <h1 class="titles text-center mb-5">
        체크하기
      </h1>
      <div class="text-center">
        <p id="ClockDisplay" class="clock" />
      </div>
    </header>
    <div>
      <div class="locationSelect">
        <v-chip
          v-for="lo in locations.length"
          :key="lo"
          class="mt-3 mx-2"
          :class="{ 'selectButton': default_campus[lo - 1], 'unSelectButton': !default_campus[lo - 1] }"
          @click="setCampus(lo)"
        >
          {{ locations[lo - 1] }}
        </v-chip>
      </div>
      <video id="face-video" width="720" height="560" autoplay muted />
    </div>
  </div>
</template>

<script>
import * as faceapi from 'face-api.js'

export default {
  asyncData ({ params }) {
    const campusRoot = params.campus

    return { campusRoot }
  },
  data: () => {
    return {
      locations: ['서울', '대전', '광주', '구미'],
      stage: ['success', 'warning', 'info'],
      default_campus: [true, false, false, false],
      selectLocation: 0
    }
  },
  mounted () {
    this.start()
    this.showTime()
    // this.getVideo()
  },
  beforeLeave (to, from, next) {
    // this.videoOff()
    // next()
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
    setCampus (v) {
      this.default_campus = this.default_campus.map(v => false)
      this.default_campus[v - 1] = true
      this.selectLocation = v - 1
      console.log(this.selectLocation)
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
        const displaySize = {
          width: video.width,
          height: video.height
        }
        faceapi.matchDimensions(canvas, displaySize)
        setInterval(async () => {
          const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
          if (detections) {
            const ctx = canvas.getContext('2d')
            ctx.drawImage(video, 0, 0, 720, 560)
            const imageURI = canvas.toDataURL('image/jpeg')
            const blob = this.dataURItoBlob(imageURI)
            const formdata = new FormData()
            formdata.append('pic_name', blob)
            formdata.append('region_id', this.selectLocation + 1)
            return this.$axios.$post('/api/recognition/', formdata)
              .then(function (data) {
                console.log(`data: ${data}`)
              })
              .catch(e => console.error(e))
          }
        }, 2000)
      })
      video.addEventListener('pause', () => {
        const stream = video.srcObject
        const tracks = stream.getTracks()
        tracks.forEach(function (track) {
          track.stop()
        })
        video.srcObject = null
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

      const time = h + ':' + m + ':' + s + ' '
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
  color: #ffffff;
  font-size: 65pt;
  font-family: 'Helvetica';
}

.describe{
  font-size: 60pt;
  color: #ffffff;
}

#face-video {
  width: 100%;
  height: 78%;
  justify-content: center;
  align-items: center;
}

canvas {
  display: None;
}

.locationSelect {
  width: 100%;
  top: 0;
  text-align: center;
  height: 50px;
}

.selectButton {
  background-color: hotpink !important;
  color: white;
}
.unSelectButton {
  background-color: white !important;
  border: 1px dashed black;
}
</style>
