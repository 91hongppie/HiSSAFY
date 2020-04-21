<template>
  <div>
    <div v-for="num in nums" :key="num" class="px-3 d-flex flex-column">
      <div>
        <v-btn :to="'/main/classes/' + num.stage + 'n' + num.location + 'n' + num.class" text x-large><h3>{{locations[num.location]}} {{num.class}}반</h3></v-btn><v-chip :color="stage[num.stage - 1]" small>{{num.stage}}기</v-chip>
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
      locations: ['서울', '대전', '광주', '구미'],
      nums: [
        {
          stage: 2,
          location: 2,
          class: 1
        },
        {
          stage: 3,
          location: 1,
          class: 4
        },
        {
          stage: 2,
          location: 3,
          class: 2
        }

      ],
      stage: ['success', 'warning', 'info']
    }
  },
  mounted () {
    this.showLine = true // showLine will only be set to true on the client. This keeps the DOM-tree in sync.
  }
}
</script>

<style scoped>
.class-box {
  display: flex;
  margin-right: 10px;
}
</style>
