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
      <v-col class="text-center">{{ student.name }}</v-col>
      <v-col class="text-center">{{ student.mark }}</v-col>
      <v-col class="text-center">{{ student.intime }}</v-col>
      <v-col class="text-center">{{ student.outtime }}</v-col>
      <v-col class="text-center">{{ student.late }}</v-col>
      <v-col class="text-center">{{ student.out }}</v-col>
    </v-row>
    {{ urlParams }}
  </div>
</template>

<script>
export default {
  mounted () {
    const urlParams = this.getUrlParams()
    return { urlParams }
  },
  methods: {
    getUrlParams () {
      const params = {}
      window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (str, key, value) { params[key] = value })
      return params
    }
  }
}
</script>

<style>

</style>
