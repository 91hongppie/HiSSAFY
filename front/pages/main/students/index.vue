<template>
  <div>
    <div class="locationSelect d-flex justify-space-around align-center jua">
      <div>
        <v-chip
          v-for="lo in locations.length"
          :key="lo"
          class="mt-3 mx-2"
          :class="{ 'selectButton': default_campus[lo - 1], 'unSelectButton': !default_campus[lo - 1] }"
          @click="setCampus(lo)"
        >
          {{ locations[lo - 1] }}
        </v-chip>
      </div>
      <v-form class="d-flex justify-center align-center">
        <v-text-field v-model="searchName" placeholder="학생 이름"></v-text-field>
        <v-btn class="mx-3 selectButton">검색</v-btn>
      </v-form>
    </div>
    <div>
      <v-row>
        <v-col class="text-center font-weight-bold">이름</v-col>
        <v-col class="text-center font-weight-bold">입실 상태</v-col>
        <v-col class="text-center font-weight-bold">평균 입실시간</v-col>
        <v-col class="text-center font-weight-bold">평균 퇴실시간</v-col>
        <v-col class="text-center font-weight-bold">지각 (회)</v-col>
        <v-col class="text-center font-weight-bold">결석 (회)</v-col>
      </v-row>
      <v-row v-for="student in searchedList" :key="student.id">
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
  layout: 'super',
  data () {
    return {
      locations: ['서울', '대전', '광주', '구미'],
      default_campus: [true, false, false, false],
      selectLocation: 0,
      searchName: '',
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
  },
  watch: {
    searchedList (searchName) {
      for (const indexNumber in this.students) {
        if (this.students[indexNumber].name.includes(searchName)) {
          this.searchedList.push(this.students[indexNumber])
        }
      }
    }
  },
  methods: {
    setCampus (v) {
      this.default_campus = this.default_campus.map(v => false)
      this.default_campus[v - 1] = true
      this.selectLocation = v - 1
    }
  }
}
</script>

<style scoped>
.selectButton {
  background-color: #2196f3 !important;
  color: white;
}
.unSelectButton {
  background-color: white !important;
  border: 1px dashed black;
}
.jua {
  font-family: 'Jua', sans-serif;
}
</style>
