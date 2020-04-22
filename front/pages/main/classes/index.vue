<template>
  <div>
    <v-form class="d-flex">
      <v-row>
        <v-col cols="3">
          <v-select
            :items="loca"
            v-model="selectedLoca"
            label="지역"
            outlined
            dense
          ></v-select>
        </v-col>
        <v-col cols="3">
          <v-select
            :items="stag"
            v-model="selectedStag"
            label="기수"
            outlined
            dense
          ></v-select>
        </v-col>
        <v-col cols="3">
          <v-select
            :items="clas"
            v-model="selectedClas"
            label="반"
            outlined
            dense
          ></v-select>
        </v-col>
        <v-col>
          <v-btn @click="searchClass" :to="'/main/classes/' + selectedStag + 'n' + selectedLoca + 'n' + selectedClas">
            검색
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  data () {
    return {
      loca: [
        {
          text: '서울',
          value: 0
        },
        {
          text: '대전',
          value: 1
        },
        {
          text: '광주',
          value: 2
        },
        {
          text: '구미',
          value: 3
        }],
      stag: [2, 3],
      clas: [1, 2, 3, 4],
      selectedStag: null,
      selectedLoca: null,
      selectedClas: null
    }
  },
  methods: {
    searchClass () {
      alert(`지역: ${this.selectedLoca}, 기수: ${this.selectedStag}, 반: ${this.selectedClas}`)
    }
  }
}
</script>

<style scoped>
div {
  padding: 10px;
}
</style>
