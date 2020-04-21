<template>
  <div class="container">
    <h1 class="text-center">등록 페이지</h1>
    <video autoplay="true">No video support in your browser</video>
    <img src="">
    <canvas style="display:none;" width="640" height="480"></canvas>
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
