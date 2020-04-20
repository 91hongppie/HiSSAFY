<template>
  <div class="classInfo">
    <a href=""><h3>대전 1반</h3></a>
    <div>
      <client-only>
        <my-doughnut v-if="showLine" :data="lineData" :options="options" style="width: 300px; height: 300px; display: inline-block;" />
      </client-only>
      <div>
        <h4 style="display: inline-block; margin: auto;">~아직 입실 전~</h4>
        <p style="display: inline-block;">HI</p>
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
      showLine: false
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
  height: 40%;
}
</style>
