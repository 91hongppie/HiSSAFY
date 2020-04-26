<template>
  <div>
    <v-form class="d-flex">
      <v-row>
        <v-col cols="3">
          <v-select
            v-model="selectedLoca"
            :items="loca"
            label="지역"
            outlined
            dense
          />
        </v-col>
        <v-col cols="3">
          <v-select
            v-model="selectedStag"
            :items="stag"
            label="기수"
            outlined
            dense
          />
        </v-col>
        <v-col cols="3">
          <v-select
            v-model="selectedClas"
            :items="clas"
            label="반"
            outlined
            dense
          />
        </v-col>
        <v-col>
          <v-btn :to="`/main/classes/${selectedStag}n${selectedLoca}n${selectedClas}/`">
            검색
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
    <div>
      {{ classData }}
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  asyncData () {

  },
  data () {
    return {
      loca: [
        {
          text: '서울',
          value: 1
        },
        {
          text: '대전',
          value: 2
        },
        {
          text: '광주',
          value: 3
        },
        {
          text: '구미',
          value: 4
        }],
      stag: [1, 2, 3],
      clas: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      selectedStag: null,
      selectedLoca: null,
      selectedClas: null,
      classData: null
    }
  }
}
</script>

<style scoped>
div {
  padding: 10px;
}
</style>
