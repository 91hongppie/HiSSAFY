<template>
  <div class="container">
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
      <video autoplay="true">No video support in your browser</video>
      <div class="chk-face">
        <div class="btns">
          <p class="describe text-center mt-5">본인 얼굴이 맞나요?</p>
          <v-btn class="yes" to="/student/completed_check" color="blue darken-1 mr-5" large>예</v-btn>
          <v-btn class="no" onclick="" color="deep-orange ml-5" large>아니오</v-btn>
        </div>
        <img class="mt-5" src="">
        <canvas style="display:none;" width="640" height="480" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted () {
    this.getVideo()
  },
  beforeLeave (to, from, next) {
    this.videoOff()
    next()
  },
  methods: {
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
          image.src = canvas.toDataURL('image/png')
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
        })
        .catch(function (err) {
          alert(err.name + ': ' + err.message)
        })
    },
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
    }
  }
}
</script>

<style>
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
