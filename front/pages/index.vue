<template>
  <div id="app" class="blue">
    <header class="text-center">
      <img src="../components/hissafyv4.png" alt="HI SSAFY LOGO" class="logo">
    </header>
    <div class="admin-btn text-center">
    </div>
    <div class="cloc text-center">
      <p id="ClockDisplay" class="clock" />
    </div>
    <div class="std-btn text-center check">
      <v-btn :to="`/student/check/`" color="green darken-2" class="mb-5 btn" large>체크하기</v-btn>
    </div>
    <div class="std-btn text-center enroll">
      <v-btn to="/student/enroll/" color="blue darken-4" class="mt-5 btn" large>얼굴 등록하기</v-btn>
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

      h = (h < 10) ? '0' + h : h
      m = (m < 10) ? '0' + m : m
      s = (s < 10) ? '0' + s : s

      const time = h + ':' + m + ':' + s
      document.getElementById('ClockDisplay').textContent = time

      setTimeout(this.showTime, 1000)
    }
  }
}
</script>

<style scoped>
header {
  margin-top: 60px;
}

.logo {
  width: 30%;
}

.clock {
  position: relative;
  color: #ffffff;
  font-size: 80pt;
  font-family: 'Helvetica';
  margin-top: 50px;
  margin-bottom: 100px;
}

.name {
  color: #ffffff;
  font-size: 100pt;
  font-family: 'Helvetica';
}

.colored {
  color: #000000;
}

.exclamation {
  font-size: 120pt;
}

.btn {
  width: 200px;
  height: 100px;
  font-size: 15pt;
  font-family: 'Noto Sans CJK KR';
  color: white;
}

.campus {
  width: 200px;
  margin-top: 50px;
  margin-bottom: 0px;
  margin-right: auto;
  margin-left: auto;

}
</style>
