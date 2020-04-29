<template>
  <div>
    <!-- 1명일 때 -->
    <v-container v-if="resultList.length === 1" class="nanumG-20">
      <v-row class="d-flex justify-center align-center jua-25">
        <v-chip color="blue lighten-2" class="mr-5" dark>
          {{ locations[resultList[0].region] }} {{ resultList[0].stage }}기
        </v-chip>
        <a class="non-a">
          {{ resultList[0].name }}
        </a>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          출석률 (%)
        </v-col>
        <v-col>
          {{ resultList[0].attendance_rate }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          평균 입실시간
        </v-col>
        <v-col>
          {{ resultList[0].avg_in_time }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          평균 퇴실시간
        </v-col>
        <v-col>
          {{ resultList[0].avg_out_time }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          지각 (회)
        </v-col>
        <v-col>
          {{ resultList[0].come_late_cnt }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          조퇴 (회)
        </v-col>
        <v-col>
          {{ resultList[0].early_left_cnt }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          사유 결석 (회)
        </v-col>
        <v-col>
          {{ resultList[0].allow_absent_day }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          임의 결석 (회)
        </v-col>
        <v-col>
          {{ resultList[0].Disallow_absent_day }}
        </v-col>
      </v-row>
    </v-container>

    <!-- 1명 이상일 때 -->
    <v-container v-else class="text-center">
      <h1 v-if="resultList.length > 1" class="text-center jua-20">세부적인 내용은 이름을 클릭해서 확인하세요</h1>
      <h1 v-else class="text-center jua-20">찾는 정보가 없습니다</h1>
      <v-row v-for="studentIndex in Math.ceil(resultList.length / 2)" :key="studentIndex" row-height="200px">
        <v-col cols="6">
          <v-container class="studentCard jua-20" height="200px">
            <v-row class="d-flex justify-center align-center">
              <v-chip color="blue lighten-2" dark class="mr-5">
                {{ locations[resultList[(studentIndex - 1) * 2].region] }} {{ resultList[(studentIndex - 1) * 2].stage }}기
              </v-chip>
              <v-btn class="jua-25" text :to="`/main/students/${resultList[(studentIndex - 1) * 2].region}&${resultList[(studentIndex - 1) * 2].name}`" :key="`${resultList[(studentIndex - 1) * 2].region}&${resultList[(studentIndex - 1) * 2].name}`">
                {{ resultList[(studentIndex - 1) * 2].name }}
              </v-btn>
            </v-row>
            <v-row>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center">
                  출석률
                </v-row>
                <v-row class="d-flex justify-center align-center">
                  <span :class="{'perfect': resultList[(studentIndex - 1) * 2].attendance_rate === 100, 'good': 100 > resultList[(studentIndex - 1) * 2].attendance_rate && resultList[(studentIndex - 1) * 2].attendance_rate > 95, 'warn': 95 >= resultList[(studentIndex - 1) * 2].attendance_rate }">
                    {{ resultList[(studentIndex - 1) * 2].attendance_rate }}
                  </span>%
                </v-row>
              </v-col>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center align-center">
                  지각
                </v-row>
                <v-row class="d-flex justify-center align-center" row-height="52px">
                  {{ resultList[(studentIndex - 1) * 2].come_late_cnt }}
                </v-row>
              </v-col>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center align-center">
                  조퇴
                </v-row>
                <v-row class="d-flex justify-center align-center" row-height="52px">
                  {{ resultList[(studentIndex - 1) * 2].early_left_cnt }}
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
        <v-col cols="6" v-if="resultList.length > ((studentIndex - 1) * 2 + 1)">
          <v-container class="studentCard jua-20">
            <v-row class="d-flex justify-center align-center">
              <v-chip color="blue lighten-2" dark class="mr-5">
                {{ locations[resultList[(studentIndex - 1) * 2 + 1].region] }} {{ resultList[(studentIndex - 1) * 2 + 1].stage }}기
              </v-chip>
              <v-btn class="jua-25" text :to="`/main/students/${resultList[(studentIndex - 1) * 2 + 1].region}&${resultList[(studentIndex - 1) * 2 + 1].name}`" :key="`${resultList[(studentIndex - 1) * 2 + 1].region}&${resultList[(studentIndex - 1) * 2 + 1].name}`">
                {{ resultList[(studentIndex - 1) * 2 + 1].name }}
              </v-btn>
            </v-row>
            <v-row>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center">
                  출석률
                </v-row>
                <v-row class="d-flex justify-center align-center">
                  <span :class="{'perfect': resultList[(studentIndex - 1) * 2 + 1].attendance_rate === 100, 'good': 100 > resultList[(studentIndex - 1) * 2 + 1].attendance_rate && resultList[(studentIndex - 1) * 2 + 1].attendance_rate > 95, 'warn': 95 >= resultList[(studentIndex - 1) * 2 + 1].attendance_rate }">
                    {{ resultList[(studentIndex - 1) * 2 + 1].attendance_rate }}
                  </span>%
                </v-row>
              </v-col>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center align-center">
                  지각
                </v-row>
                <v-row class="d-flex justify-center align-center" row-height="52px">
                  {{ resultList[(studentIndex - 1) * 2 + 1].come_late_cnt }}
                </v-row>
              </v-col>
              <v-col class="d-flex flex-column justify-space-between">
                <v-row class="d-flex justify-center align-center">
                  조퇴
                </v-row>
                <v-row class="d-flex justify-center align-center" row-height="52px">
                  {{ resultList[(studentIndex - 1) * 2 + 1].early_left_cnt }}
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  async asyncData ({ params, $axios }) {
    const conditions = params.studentList.split('&')
    let location = ''
    let name = ''
    if (conditions.length > 1) {
      if (conditions[0] === '') {
        name = conditions[1]
      } else {
        location = conditions[0]
        name = conditions[1]
      }
    } else {
      location = conditions[0]
    }

    const today = new Date()
    const year = today.getFullYear()
    const month = today.getMonth() + 1
    const studentData = await $axios.$get(`/api/checks/month/all/${year}/${month}`)
    const resultList = []
    if (location === '') {
      for (const student in studentData) {
        if (studentData[student].name.includes(decodeURI(name)) || studentData[student].student_id === name) {
          resultList.push(studentData[student])
        }
      }
    } else if (name === '') {
      for (const student in studentData) {
        if (location.includes(studentData[student].region)) {
          resultList.push(studentData[student])
        }
      }
    } else {
      for (const student in studentData) {
        if (location.includes(studentData[student].region) && (studentData[student].name.includes(decodeURI(name)) || studentData[student].student_id === name)) {
          resultList.push(studentData[student])
        }
      }
    }
    return { year, month, resultList }
  },
  data () {
    return {
      locations: ['', '서울', '대전', '광주', '구미']
    }
  }
}
</script>

<style scoped>
.studentCard {
  border: 1.5px solid black;
  border-radius: 10px;
  margin: 5px;
}
.nanumG-20 {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 20px;
}
.jua-25 {
  font-family: 'Jua', sans-serif;
  font-size: 25px;
}
.jua-20 {
  font-family: 'Jua', sans-serif;
  font-size: 20px;
}
.non-a {
  text-decoration: none;
  color: black;
}
.perfect {
  color: #2196f3;
}
.good {
  color: #2fd45b;
}
.warn {
  color: #e88a38;
}
</style>
