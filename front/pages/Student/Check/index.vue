<template>
  <div class="container" onunload="videoOff()">
    <div id="goback">
      <v-btn color="secondary mr-5" @click="goBack()">뒤로가기</v-btn>
    </div>
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
      <div class="timer">
        <p id="ClockDisplay" class="clock" />
      </div>
      <div class="video">
        <video id="face-video" width="640" height="480" autoplay muted />
        <div class="inCheck">
          <div v-for="studentName in studentNames[selectLocation].length" :key="studentName.id">
            {{ studentNames[selectLocation][studentName-1] }}
            {{ studentIds[selectLocation][studentName-1] }}
            님이 입실하셨습니다.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as faceapi from 'face-api.js'

export default {
  data: () => {
    return {
      locations: ['서울', '대전', '구미', '광주'],
      stage: ['success', 'warning', 'info'],
      default_campus: [true, false, false, false],
      selectLocation: 0,
      studentNames: [[], [], [], []],
      studentIds: [[], [], [], []]
    }
  },
  watch: {
    studentNames: {
      deep: true,
      handler () {
      }
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
    goBack () {
      document.querySelector('video').pause()
      this.$router.push('/')
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
            ctx.drawImage(video, 0, 0, 640, 480)
            const imageURI = canvas.toDataURL('image/jpeg')
            const blob = this.dataURItoBlob(imageURI)
            const formdata = new FormData()
            formdata.append('pic_name', blob)
            formdata.append('region_id', this.selectLocation + 1)
            this.$axios.$post('/api/recognition/', formdata)
              .then((data) => {
                for (let i = 0; i < data.length; i++) {
                  const element = data[i][0]
                  console.log(element.region)
                  if (this.studentNames[element.region - 1].length === 20) {
                    this.studentNames[element.region - 1] = this.studentNames[element.region - 1].slice(1, this.studentNames[element.region - 1].length)
                    this.studentIds[element.region - 1] = this.studentIds[element.region - 1].slice(1, this.studentIds[element.region - 1].length)
                  }
                  if (!this.studentNames[element.region - 1].includes(element.name)) {
                    this.studentNames[element.region - 1].push(element.name)
                    this.studentIds[element.region - 1].push(element.student_id)
                  }
                }
              })
              .catch(e => console.error(e))
            console.log(this.studentNames)
            console.log(this.studentIds)
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
    }
  }
}
</script>

<style scoped lang="scss">
#goback {
  margin-top: 30px;
  margin-bottom: 30px;
}

.titles {
  font-size: 100pt;
  color: #ffffff;
}

.timer {
  display: flex;
  width: 100%;
  justify-content: center;
}

.clock {
  position: absolute;
  color: #ffffff;
  font-size: 45pt;
  font-family: 'Helvetica';
}

.describe{
  font-size: 60pt;
  color: #ffffff;
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

#goback {
  display: flex;
  width: 100%;
  align-content: center;
  justify-content: center;
}
@media ( min-width: 1050px ) {
  .video {
    display: flex;
    width: 100%;
    justify-content: center;
  }
    #face-video {
    width: 50%;
    height: 50%;
  }
    .inCheck {
    width: 100%;
    height: 200px;
    position: absolute;
    overflow: auto;
    margin-left: 20px;
    color: #ffffff;
  }
}

@media ( max-width: 1050px) {
  .video {
    width: 100%;
    justify-content: center;
  }
  #face-video {
    display: block;
    width: 100%;
    height: 50%;
  }
  .inCheck {
    width: 100%;
    height: 200px;
    overflow: auto;
    position: relative;
    margin-left: 20px;
    color: #ffffff;
  }
}

</style>
