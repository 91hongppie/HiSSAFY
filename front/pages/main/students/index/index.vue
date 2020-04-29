<template>
  <div class="d-flex flex-column align-center">
    <h1 class="jua-30">학생 또는 학번을 검색해주세요</h1>
    <h2 class="jua-20">(지역을 선택하면 해당하는 지역의 학생을 검색합니다)</h2>
    <v-container>
      <v-row>
        <v-col class="text-center font-weight-bold">이름</v-col>
        <v-col class="text-center font-weight-bold">입실 상태</v-col>
        <v-col class="text-center font-weight-bold">평균 입실시간</v-col>
        <v-col class="text-center font-weight-bold">평균 퇴실시간</v-col>
        <v-col class="text-center font-weight-bold">지각 (회)</v-col>
        <v-col class="text-center font-weight-bold">결석 (회)</v-col>
      </v-row>
      <v-row v-for="student in studentList" :key="student.id">
        <v-col class="text-center"><nuxt-link :to="`/main/students/${student.id}`">{{ student.name }}</nuxt-link></v-col>
        <v-col class="text-center">{{ student.mark }}</v-col>
        <v-col class="text-center">{{ student.intime }}</v-col>
        <v-col class="text-center">{{ student.outtime }}</v-col>
        <v-col class="text-center">{{ student.late }}</v-col>
        <v-col class="text-center">{{ student.out }}</v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  async asyncData ({ params, $axios }) {
    console.log(params)
    const today = new Date()
    const year = today.getFullYear()
    const month = today.getMonth() + 1
    const studentList = await $axios.$get(`/api/checks/month/all/${year}/${month}/`)
    return { studentList, year, month }
  }
}
</script>

<style scoped>
.jua-30 {
  font-family: 'Jua', sans-serif;
  font-size: 30px;
}
.jua-20 {
  font-family: 'Jua', sans-serif;
  font-size: 20px;
}
</style>
