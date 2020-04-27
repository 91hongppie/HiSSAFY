<template>
  <div id="app" class="blue">
    <header class="mt-5">
      <h1 class="name text-center">
        <span class="colored">HI</span> SSAFY!
      </h1>
    </header>
    <div class="admin-btn text-center">
      <v-btn class="justify-center" color="warning" to="/main">
        Admin Page
      </v-btn>
    </div>
    <div class="cloc text-center">
      <p id="ClockDisplay" class="clock" />
    </div>
    <div class="std-btn text-center">
      <v-btn to="/student/check" color="purple" class="mr-5 btn" large>체크하기</v-btn>
      <v-btn to="/student/enroll" color="pink" class="ml-5 btn" large>얼굴 등록하기</v-btn>
    </div>
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

      // const time = h + ':' + m + ':' + s + ' ' + session
      const time = h + ':' + m + ':' + s + ' '
      document.getElementById('ClockDisplay').textContent = time

      setTimeout(this.showTime, 1000)
    }
  }
}
</script>

<style scoped>
.clock {
  position: relative;
  /* top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%); */
  color: #ffffff;
  font-size: 80pt;
  font-family: 'Helvetica';
  /* letter-spacing: 3px; */
  margin-top: 100px;
  margin-bottom: 100px;
}

.name {
  color: #ffffff;
  font-size: 100pt;
  font-family: 'Helvetica';
}

.colored {
  color: #0f4c81;
}

.btn {
  width: 200px;
  height: 100px;
  font-size: 15pt;
  font-family: 'Noto Sans CJK KR';
  color: white;
}
</style>
