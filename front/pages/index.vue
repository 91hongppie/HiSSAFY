<template>
  <div id="app" class="blue">
    <header class="mt-5">
      <h1 class="text-center">HI SSAFY!</h1>
    </header>
    <div id="ClockDisplay" class="clock" onload="showTime()"></div>
    <div class="admin-btn text-center mt-5 mb-5">
      <v-btn class="justify-center" color="warning" to="/main">
        Admin Page
      </v-btn>
    </div>
    <div class="std-btn text-center">
      <v-btn to="/student/check" color="purple">체크하기</v-btn>
      <v-btn to="/student/enroll" color="pink">얼굴 등록하기</v-btn>
    </div>
  </div>
</template>

<script>
export default {

}

// function showTime () {
//   const date = new Date()
//   let h = date.getHours() // 0 - 23
//   let m = date.getMinutes() // 0 - 59
//   let s = date.getSeconds() // 0 - 59
//   let session = 'AM'

//   if (h === 0) {
//     h = 12
//   }

//   if (h > 12) {
//     h = h - 12
//     session = 'PM'
//   }

//   h = (h < 10) ? '0' + h : h
//   m = (m < 10) ? '0' + m : m
//   s = (s < 10) ? '0' + s : s

//   const time = h + ':' + m + ':' + s + ' ' + session
//   // document.getElementById('ClockDisplay').innerText = time
//   document.getElementById('ClockDisplay').textContent = time

//   setTimeout(showTime, 1000)
// }

// showTime()
</script>

<style>
.clock {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    color: #17D4FE;
    font-size: 60px;
    font-family: Orbitron;
    letter-spacing: 7px;
}
</style>
