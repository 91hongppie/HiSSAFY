<template>
  <div>
    <h1>{{className}}</h1>
    <client-only>
      <my-line v-if="showLine" :data="lineData" :options="options" style="display: inline-block; width: 700px; height: 200px;" />
    </client-only>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  asyncData () {
    const lineData = {
      labels: ['4월 1일', '4월 2일', '4월 3일'],
      datasets: [{
        label: '출석 현황',
        data: [100.0, 100.0, 98.0],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(120, 200, 132, 1)'
        ],
        fill: false,
        borderCapStyle: 'round'
      }]
    }
    const options = {
      legend: {
        display: true,
        position: 'bottom'
      },
      scales: {
        yAxes: [{
          stacked: true
        }]
      }
    } // some options
    return { lineData, options }
  },
  data () {
    return {
      showLine: false,
      className: '대전 1반'
    }
  },
  mounted () {
    this.showLine = true
  }
}
</script>

<style>

</style>
