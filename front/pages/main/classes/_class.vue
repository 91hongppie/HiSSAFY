<template>
  <div class="text-center">
    <div class="noteStyle">
      <h1 class="gugi-30">{{ className }}</h1>
      <div class="text-center nanumG">
        <v-row class="underlineTitle">
          <v-col class="font-weight-bold">이름</v-col>
          <v-col class="font-weight-bold">입실시간</v-col>
          <v-col class="font-weight-bold">퇴실시간</v-col>
          <v-col class="font-weight-bold">상태</v-col>
        </v-row>
        <v-row v-for="student in classData" :key="student.student_id" class="underlineBody">
          <v-col>{{ student.name }}</v-col>
          <v-col>{{ student.in_time? student.in_time : '-' }}</v-col>
          <v-col>{{ student.out_time? student.out_time : '-' }}</v-col>
          <v-col>{{ setStat(student.is_late, student.is_early, student.status) }}</v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData ({ params, $axios }) {
    // 기수, 지역, 반
    const classRoot = params.class.split('n')
    const classData = await $axios.$get(`/api/checks/daily/${classRoot[0]}/${classRoot[1]}/${classRoot[2]}`)

    return { classData, classRoot }
  },
  data () {
    return {
      className: '',
      statName: ['정상 입실', '지각', '조퇴', '결석'],
      locations: ['서울', '대전', '광주', '구미']
    }
  },
  mounted () {
    this.className = `${this.classRoot[0]}기 ${this.locations[this.classRoot[1] - 1]} ${this.classRoot[2]}반`
  },
  methods: {
    setStat (late, early, stat) {
      if (stat === 0) {
        return '결석'
      } else if (late === true) {
        return '지각'
      } else if (early === true) {
        return '조퇴'
      } else {
        return '정상 입실'
      }
    }
  }
}
</script>

<style scoped>
div {
  margin: 5px 20px;
}
.noteStyle {
  margin-top: 20px;
  padding-top: 15px;
  padding-bottom: 20px;
  background-color: rgb(255, 233, 143);
  border-radius: 5px;
}
.gugi-30 {
  font-family: 'Gugi', cursive;
  font-size: 30px;
}
.nanumG {
  font-family: 'Nanum Gothic', sans-serif;
}
.underlineTitle {
  border-bottom: 2px solid black;
}
.underlineBody {
  border-bottom: 1.5px solid rgba(250, 125, 125, 0.5)
}
</style>
