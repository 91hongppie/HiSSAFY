<template>
  <div>
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
          <v-btn :to="'/main/classes/' + st + 'n' + default_campus.indexOf(true) + 'n' + cl" text x-large>
            <h3>{{ locations[default_campus - 1] }} {{ cl }}반</h3>
          </v-btn>
          <v-chip :color="stage[st - 1]" small>
            {{ st }}기
          </v-chip>
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
          <div class="text-center">
            <h3>출석 안 한 사람 <v-chip dark small>{{ selectedData[st][cl]['uncheck'].length }}명</v-chip></h3>
            <p><span v-for="name in selectedData[st][cl]['uncheck']" :key="selectedData[st][cl]['uncheck'].indexOf(name)">{{ name }} </span></p>
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
      locations: ['서울', '대전', '광주', '구미'],
      // 지역 { 기수 { 반 } }
      totalData: {
        1: {
          1: {
            3: {
              memebers: 2,
              check: [],
              uncheck: ['장동건', '전미도']
            }
          },
          2: {
            2: {
              memebers: 1,
              check: [],
              uncheck: ['장범준']
            }
          }
        },
        2: {
          1: {
            3: {
              memebers: 1,
              check: [],
              uncheck: ['휘성']
            }
          },
          2: {
            1: {
              memebers: 38,
              check: ['캡틴'],
              uncheck: [
                '아연맨',
                '스파이디',
                '토르',
                '강동원',
                '강동원',
                '김무열',
                '김범수',
                '김우빈',
                '김우빈',
                '김태리',
                '김혜수',
                '남주혁',
                '남주혁',
                '박보검',
                '박보검',
                '박서준',
                '박서준',
                '서강준',
                '서강준',
                '송민호',
                '아이린',
                '아이유',
                '유아인',
                '유아인',
                '유재석',
                '유재석',
                '은지원',
                '은지원',
                '이민호',
                '이민호',
                '이상민',
                '이수근',
                '이정재',
                '이주빈',
                '이효리',
                '전미도',
                '휘성'
              ]
            }
          }
        },
        3: {
          1: {
            2: {
              members: 3,
              check: [],
              uncheck: ['조정석', '휘성', '휘성']
            }
          }
        },
        4: {
          1: {
            3: {
              memebers: 1,
              check: [],
              uncheck: ['하정우']
            }
          },
          2: {
            4: {
              memebers: 1,
              check: [],
              uncheck: ['지드래곤']
            }
          }
        },
        5: {
          3: {
            1: {
              memebers: 1,
              check: [],
              uncheck: ['조정석']
            }
          }
        }
      },
      stage: ['success', 'warning', 'info'],
      default_campus: [true, false, false, false]
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
</style>
