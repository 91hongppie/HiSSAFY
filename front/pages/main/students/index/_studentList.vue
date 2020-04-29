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
          {{ resultList[0].intime }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          평균 퇴실시간
        </v-col>
        <v-col>
          {{ resultList[0].outtime }}
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
      <v-row v-for="studentIndex in Math.ceil(resultList.length / 2)" :key="studentIndex" row-height="200px">
        <v-col cols="6">
          <v-container class="studentCard jua-20" height="200px">
            <v-row class="d-flex justify-center align-center">
              <v-chip color="blue lighten-2" dark class="mr-5">
                {{ locations[resultList[(studentIndex - 1) * 2].region] }} {{ resultList[(studentIndex - 1) * 2].stage }}기
              </v-chip>
              {{ resultList[(studentIndex - 1) * 2].name }}
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
              {{ resultList[(studentIndex - 1) * 2 + 1].name }}
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
  // async asyncData ({ params, $axios }) {
  //   const conditions = params.studentList.split('&')
  //   let location = ''
  //   let name = ''
  //   if (conditions.length > 1) {
  //     console.log(conditions)
  //     if (conditions[0] === '') {
  //       console.log('이름만!')
  //       name = conditions[1]
  //     } else {
  //       console.log('둘다!!')
  //       location = conditions[0]
  //       name = conditions[1]
  //     }
  //   } else {
  //     console.log('지역!!!!!')
  //     location = conditions[0]
  //     console.log('wowo')
  //   }

  //   const today = new Date()
  //   const year = today.getFullYear()
  //   const month = today.getMonth() + 1
  //   const studentData = await $axios.$get(`/api/checks/month/all/${year}/${month}`)
  //   const resultList = []
  //   if (location === '') {
  //     for (const student in studentData) {
  //       if (studentData[student].name.includes(decodeURI(name)) || studentData[student].student_id === name) {
  //         resultList.push(studentData[student])
  //       }
  //     }
  //   } else if (name === '') {
  //     for (const student in studentData) {
  //       if (location.includes(studentData[student].region)) {
  //         resultList.push(studentData[student])
  //       }
  //     }
  //   } else {
  //     for (const student in studentData) {
  //       if (location.includes(studentData[student].region) && (studentData[student].name.includes(decodeURI(name)) || studentData[student].student_id === Number(name))) {
  //         resultList.push(studentData[student])
  //       }
  //     }
  //   }
  //   console.log(resultList)
  //   return { year, month, resultList }
  // },
  data () {
    return {
      locations: ['', '서울', '대전', '광주', '구미'],
      resultList: [
        {
          region: 2,
          stage: 1,
          student_id: '0234999',
          name: '홍길금',
          attendance_rate: 100,
          intime: '',
          outtime: '',
          come_late_cnt: 1,
          early_left_cnt: 0,
          allow_absent_day: 0,
          Disallow_absent_day: 1
        },
        {
          region: 2,
          stage: 1,
          student_id: '0234989',
          name: '홍길은',
          attendance_rate: 98,
          intime: '',
          outtime: '',
          come_late_cnt: 1,
          early_left_cnt: 0,
          allow_absent_day: 0,
          Disallow_absent_day: 1
        },
        {
          region: 2,
          stage: 1,
          student_id: '0234980',
          name: '홍길동',
          attendance_rate: 94,
          intime: '',
          outtime: '',
          come_late_cnt: 1,
          early_left_cnt: 0,
          allow_absent_day: 0,
          Disallow_absent_day: 0
        }
      ]
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
