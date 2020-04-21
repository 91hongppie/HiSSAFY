<template>
  <div>
    <header class="mt-5">
      <h1 class="name text-center">
        <span class="colored">HI</span> SSAFY!
      </h1>
    </header>
    <div>
      <p id="ClockDisplay" class="clock" onload="showTime()" />
    </div>
      <v-btn to="/student/check" color="purple">체크하기</v-btn>
      <v-btn to="/student/enroll" color="pink">얼굴 등록하기</v-btn>
  </div>
</template>

<script>
export default {
  mounted () {
    this.showTime()
  },

  methods: {
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
#app, body {
  background-color: #1b262c;
}

.clock {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    color: #706c61;
    font-size: 100px;
    font-family: 'Helvetica';
    /* letter-spacing: 3px; */
}

.name {
  color: #ffffff;
  font-size: 100px;
  font-family: 'Helvetica';
}

.colored {
  color: #0f4c81;
}

.btns {
  color: #e1f4f3;
}
</style>
