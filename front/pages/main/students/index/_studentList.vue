<template>
  <div>
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

<style>

</style>
