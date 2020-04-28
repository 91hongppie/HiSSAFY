<template>
  <div>
    <v-row class="text-center">
      <v-col cols="2">
        {{ year }} 년
      </v-col>
      <v-col cols="2">
        <v-select
          v-model="selectMonth"
          :items="months"
          solo
          suffix="월"
          dense
        />
      </v-col>
      <v-col cols="8">{{ studentData.name }}의 기록</v-col>
    </v-row>
    {{ studentData }}
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData ({ params, $axios }) {
    const studentId = params.student
    const today = new Date()
    const year = today.getFullYear()
    const month = today.getMonth() + 1
    const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    months.length = month
    const studentData = await $axios.$get(`/api/checks/month/student/${studentId}/${year}/${month}`)
    return { year, month, studentData: studentData[0], months }
  },
  mounted () {
    this.selectMonth = this.month
  },
  watch: {
    selectMonth () {
      this.$axios.$get(`/api/checks/month/student/${this.studentData.student_id}/${this.year}/${this.selectMonth}`)
        .then((response) => {
          this.studentData = response.data[0]
        })
    }
  },
  data () {
    return {
      selectMonth: ''
    }
  }
}
</script>

<style>

</style>
