<template>
  <div>
    <v-container v-if="resultList.length === 1">
      <v-row>
        <v-col>
          {{ locations[resultList[0].region] }} {{ resultList[0].stage }}기
        </v-col>
      </v-row>
      <v-row>
        <v-col class="font-weight-bold">
          이름
        </v-col>
        <v-col>
          {{ resultList[0].name }}
        </v-col>
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
    <v-container v-else v-for="student in resultList" :key="student.id" class="text-center studentCard">
      <v-row>
        <v-col>
          {{ locations[student.region] }} {{ student.stage }}기
        </v-col>
      </v-row>
      <v-row>
        <v-col class="font-weight-bold">
          이름
        </v-col>
        <v-col>
          {{ student.name }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          출석률 (%)
        </v-col>
        <v-col>
          {{ student.attendance_rate }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          평균 입실시간
        </v-col>
        <v-col>
          {{ student.intime }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          평균 퇴실시간
        </v-col>
        <v-col>
          {{ student.outtime }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          지각 (회)
        </v-col>
        <v-col>
          {{ student.come_late_cnt }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          조퇴 (회)
        </v-col>
        <v-col>
          {{ student.early_left_cnt }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          사유 결석 (회)
        </v-col>
        <v-col>
          {{ student.allow_absent_day }}
        </v-col>
      </v-row>

      <v-row class="text-center">
        <v-col class="font-weight-bold">
          임의 결석 (회)
        </v-col>
        <v-col>
          {{ student.Disallow_absent_day }}
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
      console.log(conditions)
      if (conditions[0] === '') {
        console.log('이름만!')
        name = conditions[1]
      } else {
        console.log('둘다!!')
        location = conditions[0]
        name = conditions[1]
      }
    } else {
      console.log('지역!!!!!')
      location = conditions[0]
      console.log('wowo')
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
        if (location.includes(studentData[student].region) && (studentData[student].name.includes(decodeURI(name)) || studentData[student].student_id === Number(name))) {
          resultList.push(studentData[student])
        }
      }
    }
    console.log(resultList)
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
</style>
