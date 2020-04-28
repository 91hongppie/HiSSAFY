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
      <div v-for="student in students" :key="student.id">
        {{ student }}
      </div>
    </div>
  </div>
</template>

<script>
import * as faceapi from 'face-api.js'

export default {
  data: () => {
    return {
      locations: ['서울', '대전', '광주', '구미'],
      stage: ['success', 'warning', 'info'],
      default_campus: [true, false, false, false],
      selectLocation: 0,
      students: []
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
            ctx.drawImage(video, 0, 0, 720, 560)
            const imageURI = canvas.toDataURL('image/jpeg')
            const blob = this.dataURItoBlob(imageURI)
            const formdata = new FormData()
            formdata.append('pic_name', blob)
            formdata.append('region_id', this.selectLocation + 1)
            return this.$axios.$post('/api/recognition/', formdata)
              .then(function (data) {
                if (data.length >= 1) {
                  for (let i = 0; i < data.length; i++) {
                    const element = data[i]
                    console.log(element[0].name)
                    this.students.append(element[0].name)
                  }
                }
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
    showTime () {
      const date = new Date()
      let h = date.getHours() // 0 - 23
      let m = date.getMinutes() // 0 - 59
      let s = date.getSeconds() // 0 - 59
      // let session = 'AM'

      // if (h === 0) {
      //   h = 12
      // }

      // if (h > 12) {
      //   h = h - 12
      //   session = 'PM'
      // }

      h = (h < 10) ? '0' + h : h
      m = (m < 10) ? '0' + m : m
      s = (s < 10) ? '0' + s : s

      const time = h + ':' + m + ':' + s + ' '
      // const time = h + ':' + m + ':' + s + ' ' + session
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

<style scoped lang="scss">
.titles {
  font-size: 100pt;
  color: #ffffff;
}

.clock {
  position: relative;
  color: #ffffff;
  font-size: 65pt;
  font-family: 'Helvetica';
  /* letter-spacing: 3px; */
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

.example-modal-content {
  height: 100%;
  box-sizing: border-box;
  padding: 10px;
  font-size: 13px;
  overflow: auto;
}

button.btn {
  outline: none;
  background: white;
  border: 0;
  padding: 10px 18px;
  cursor: pointer;
  border-radius: 3px;

  color: white;

  box-shadow: 0 4px 8px rgba(#20a0ff, .3);
  background: #4db3ff;

  font-weight: 600;

  border-radius: 3px;

  min-width: 90px;

  margin-bottom: 8px;
  margin-top: 8px;
  margin-right: 8px;

  &:hover {
    background: #20a0ff;
  }

  &.green {
    box-shadow: 0 4px 8px rgba(#50C9BA, .3);
    background: #50C9BA;

    &:hover {
     background: mix(#50C9BA, black, 95%);
    }
  }

  &.red {
    box-shadow: 0 4px 8px rgba(#F21368, .3);
    background: #F21368;

    &:hover {
      background: mix(#F21368, black, 95%);
    }
  }
}
</style>
