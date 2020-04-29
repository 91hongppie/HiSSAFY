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
          <v-col class="font-weight-bold">이름</v-col>
          <v-col class="font-weight-bold">입실시간</v-col>
          <v-col class="font-weight-bold">퇴실시간</v-col>
          <v-col class="font-weight-bold">상태</v-col>
        </v-row>
        <v-row v-for="studentIndex in Math.ceil(classData.length / 2)" :key="studentIndex" class="underlineBody">
          <v-col>{{ classData[(studentIndex - 1) * 2].name }}</v-col>
          <v-col>{{ classData[(studentIndex - 1) * 2].in_time ? classData[(studentIndex - 1) * 2].in_time : '-' }}</v-col>
          <v-col>{{ classData[(studentIndex - 1) * 2].out_time ? classData[(studentIndex - 1) * 2].out_time : '-' }}</v-col>
          <v-col>{{ setStat(classData[(studentIndex - 1) * 2].is_late, classData[(studentIndex - 1) * 2].is_early, classData[(studentIndex - 1) * 2].status) }}</v-col>
          <v-col>{{ classData.length > studentIndex * 2 - 1 ? (classData[(studentIndex * 2) - 1].name ? classData[(studentIndex * 2) - 1].name : '-' ) : '' }}</v-col>
          <v-col>{{ classData.length > studentIndex * 2 - 1 ? (classData[(studentIndex * 2) - 1].in_time ? classData[(studentIndex * 2) - 1].in_time : '-' ) : '-' }}</v-col>
          <v-col>{{ classData.length > studentIndex * 2 - 1 ? (classData[(studentIndex * 2) - 1].out_time ? classData[(studentIndex * 2) - 1].out_time : '-' ) :'-' }}</v-col>
          <v-col>{{ classData.length > studentIndex * 2 - 1 ? setStat(classData[(studentIndex * 2) - 1].is_late, classData[(studentIndex * 2) - 1].is_early, classData[(studentIndex * 2) - 1].status) : '' }}</v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'super',
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
  margin: 5px 15px;
}
div.col {
  margin: 0;
}
.noteStyle {
  padding-top: 10px;
  padding-bottom: 10px;
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
