<template>
  <div class="container blue">
    <header>
      <h1 class="titles text-center mb-5">
        얼굴 등록하기
      </h1>
      <p class="describe text-center">얼굴을 중앙에 두고 터치합니다.</p>
    </header>
    <div class="screens text-center">
      <video autoplay="true">No video support in your browser</video>
      <div class="chk-face">
        <div class="btns">
          <p class="describe text-center mt-5">본인 얼굴이 맞나요?</p>
          <v-btn class="yes" to="/student/completed_enroll" color="success mr-5" large>예</v-btn>
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
    check () {
      if (confirm('본인이 맞습니까?')) {
        location.to = '/completed_enroll'
      }
    }
  }
}
// function enrollOrNot () {
//   if (confirm('등록하시겠습니까?')) {
//     location.to='/completed_enroll'
//   }
//   else {
//     return
//   }
// }
</script>

<style scoped>
.titles {
  font-size: 100pt;
  color: #ffffff;
}

.describe {
  font-size: 60pt;
  color: #ffffff;
}
</style>
