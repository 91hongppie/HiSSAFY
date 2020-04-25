<template>
  <div class="jua">
    <div class="locationSelect">
      <v-chip
        v-for="lo in locations.length"
        :key="lo"
        class="mt-3 mx-2"
        :class="{ 'selectButton': default_campus[lo - 1], 'unSelectButton': !default_campus[lo - 1] }"
        @click="setCampus(lo)"
      >
        {{ locations[lo - 1] }}
      </v-chip>
    </div>
    <div v-for="st in Object.keys(selectedData)" :key="`data-` + st" class="px-3 d-flex flex-column mx-0 statNow">
      <!-- 기수 -->
      <div v-for="cl in Object.keys(selectedData[st])" :key="`${st}-${cl}`">
        <div>
          <v-chip :color="stage[st - 1]" small>
            {{ st }}기
          </v-chip>
          <v-btn :to="`/main/classes/${st}n${default_campus.indexOf(true) + 1}n${cl}`" text>
            <h3>{{ locations[selectLocation] }} {{ cl }}반</h3>
          </v-btn>
        </div>
        <!-- 차트 -->
        <div class="classBox">
          <my-doughnut
            v-if="showLine"
            :data="setChartData(selectedData[st][cl]['check'].length, selectedData[st][cl]['uncheck'].length)"
            :options="options"
            :location="default_campus.findIndex(isTrue) + 1"
            style="width: 300px; height: 300px; display: inline-block;"
          />
          <!-- 출석 안 한 사람 -->
          <div class="text-center px-5 mx-10" style="width: 100%;">
            <h3 class="gugi-30">출석 안 한 사람 <v-chip dark class="jua" :class="{ 'red': selectedData[st][cl]['uncheck'].length > 20, 'green' : selectedData[st][cl]['uncheck'].length > 4 && selectedData[st][cl]['uncheck'].length <= 20, 'blue': selectedData[st][cl]['uncheck'].length >= 0 && selectedData[st][cl]['uncheck'].length <= 4 }">{{ selectedData[st][cl]['uncheck'].length }}명</v-chip></h3>
            <div class="yetList">
              <v-row v-for="num in (Math.ceil(selectedData[st][cl]['uncheck'].length / 8))" :key="num">
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 1] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 2] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 3] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 4] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 5] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 6] }}</v-col>
                <v-col class="rowConfig">{{ selectedData[st][cl]['uncheck'][(num - 1) * 8 + 7] }}</v-col>
              </v-row>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData ({ $axios }) {
    const daily = await $axios.$get('/api/checks/')
    const chartData = {
      labels: ['출석', '미출석'],
      datasets: [{
        label: '출석 현황',
        data: [14, 10],
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
    return { chartData, options, daily }
  },
  data () {
    return {
      showLine: false,
      // 지역 { 기수 { 반 } }
      locations: ['서울', '대전', '광주', '구미'],
      stage: ['success', 'warning', 'info'],
      default_campus: [true, false, false, false],
      selectLocation: 1
    }
  },
  computed: {
    selectedData () {
      const findTrue = (element) => { return element === true }
      const locationValue = this.default_campus.findIndex(findTrue)
      return this.daily[locationValue + 1]
    }
  },
  mounted () {
    this.showLine = true // showLine will only be set to true on the client. This keeps the DOM-tree in sync.
  },
  methods: {
    isTrue (v) {
      return v === true
    },
    setCampus (v) {
      this.default_campus = this.default_campus.map(v => false)
      this.default_campus[v - 1] = true
      this.selectLocation = v - 1
    },
    setChartData (c, uc) {
      const temp = {
        labels: ['출석', '미출석'],
        datasets: [{
          label: '출석 현황',
          data: [c, uc],
          backgroundColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132, 1)'
          ]
        }]
      }
      return temp
    }
  }
}
</script>

<style scoped>
.classBox {
  display: flex;
  margin-right: 10px;
  width: 100%;
}
.locationSelect {
  width: 100%;
  position: fixed;
  top: 0;
  height: 50px;
}
.statNow {
  margin-top: 50px;
}
.selectButton {
  background-color: hotpink !important;
  color: white;
}
.unSelectButton {
  background-color: white !important;
  border: 1px dashed black;
}
.yetList {
  border: 2px solid black;
  border-radius: 10px;
  height: 80%;
  padding: 5px;
}
.jua {
  font-family: 'Jua', sans-serif;
}
.gugi-30 {
  font-family: 'Gugi', cursive;
  font-size: 30px;
  margin-bottom: 10px;
}
.rowConfig {
  padding: 6px;
  text-align: center;
}
</style>
