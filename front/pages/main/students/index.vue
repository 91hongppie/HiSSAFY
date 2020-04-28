<template>
  <div>
    <h1>학생들 정보 목록</h1>
    <div>
      <v-row>
        <v-col class="text-center font-weight-bold">이름</v-col>
        <v-col class="text-center font-weight-bold">입실 상태</v-col>
        <v-col class="text-center font-weight-bold">평균 입실시간</v-col>
        <v-col class="text-center font-weight-bold">평균 퇴실시간</v-col>
        <v-col class="text-center font-weight-bold">지각 (회)</v-col>
        <v-col class="text-center font-weight-bold">결석 (회)</v-col>
      </v-row>
      <v-row v-for="student in students" :key="student.id">
        <v-col class="text-center"><nuxt-link :to="`/main/students/${student.id}`">{{ student.name }}</nuxt-link></v-col>
        <v-col class="text-center">{{ student.mark }}</v-col>
        <v-col class="text-center">{{ student.intime }}</v-col>
        <v-col class="text-center">{{ student.outtime }}</v-col>
        <v-col class="text-center">{{ student.late }}</v-col>
        <v-col class="text-center">{{ student.out }}</v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  data () {
    return {
      students: [
        {
          id: '0233100',
          name: '홍길동',
          mark: 1,
          intime: '08:11:20',
          outtime: '19:54:34',
          late: 1,
          out: 0
        },
        {
          id: '0233101',
          name: '홍길은',
          mark: 1,
          intime: '08:40:50',
          outtime: '18:00:08',
          late: 1,
          out: 1
        },
        {
          id: '0233102',
          name: '홍길금',
          mark: 1,
          intime: '08:59:20',
          outtime: '18:00:03',
          late: 2,
          out: 2
        }
      ]
    }
  }
}
</script>

<style>

</style>
