<template>
  <div>
    <h1>{{ className }}</h1>
    <client-only>
      <my-line v-if="showLine" :data="lineData" :options="options" style="display: inline-block; width: 700px; height: 200px;" />
    </client-only>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  asyncData ({ params }) {
    const lineData = {
      labels: ['4월 1일', '4월 2일', '4월 3일', '4월 4일'],
      datasets: [{
        label: '출석률',
        data: [100.0, 100.0, 98.0, 100.0],
        borderColor: [
          'rgba(54, 162, 235, 1)'
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
    return { lineData, options, classNumber: params.class }
  },
  data () {
    return {
      showLine: false,
      locations: ['서울', '대전', '광주', '구미'],
      className: ''
    }
  },
  mounted () {
    this.showLine = true
    const tmp = this.classNumber.split('n')
    this.className = `${tmp[0]}기 ${this.locations[tmp[1]]} ${tmp[2]}반`
  }
}
</script>

<style scoped>
div {
  padding: 10px;
}
</style>
