<template>
  <div class="classInfo">
    <div v-for="num in nums" :key="num" class="px-3 d-flex flex-column">
      <div>
        <v-btn to="/main/dj1st" text x-large><h3>대전 1반</h3> <v-chip outlined>2기</v-chip></v-btn>
        <v-btn class="white--text" x-small color="pink">알림</v-btn>
      </div>
      <div class="class-box">
        <client-only>
          <my-doughnut v-if="showLine" :data="lineData" :options="options" style="width: 300px; height: 300px; display: inline-block;" />
        </client-only>
        <div class="text-center">
          <h3>출석 안 한 사람</h3>
          <p><span v-for="member in members" :key="member">{{member}} </span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  layout: 'admin',
  asyncData () {
    const lineData = {
      labels: ['출석', '미출석'],
      datasets: [{
        label: '출석 현황',
        data: [20, 14],
        backgroundColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)'
        ]
      }]
    }
    const options = {
      legend: {
        display: true,
        position: 'bottom'
      }
    } // some options
    return { lineData, options }
  },
  data () {
    return {
      showLine: false,
      members: ['길현', '규홍', '현호', '선행'],
      nums: [1, 2, 3]
    }
  },
  mounted () {
    this.showLine = true // showLine will only be set to true on the client. This keeps the DOM-tree in sync.
  }
}
</script>

<style>
.classInfo {
  padding: 10px;
  height: 50%;
}
.class-box {
  display: flex;
  margin-right: 10px;
}
</style>
