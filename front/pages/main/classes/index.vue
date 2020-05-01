<template>
  <div>
    <v-form class="d-flex justify-center">
      <v-row class="jua pl-12 ml-12">
        <v-col>
          <v-select
            v-model="selectClass.location"
            :items="loca"
            label="지역"
            outlined
            dense
          />
        </v-col>
        <v-col>
          <v-select
            v-model="selectClass.stage"
            :items="stag"
            label="기수"
            outlined
            dense
          />
        </v-col>
        <v-col>
          <v-select
            v-model="selectClass.classNumber"
            :items="clas"
            label="반"
            outlined
            dense
          />
        </v-col>
        <v-col>
          <v-btn :to="`/main/classes/${selectClass.stage}n${selectClass.location}n${selectClass.classNumber}`">
            확인
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
    <div>
      <NuxtChild :key="$route.params.class" />
    </div>
  </div>
</template>

<script>
export default {
  layout: 'super',
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
          text: '구미',
          value: 3
        },
        {
          text: '광주',
          value: 4
        }],
      stag: [1, 2, 3],
      clas: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      selectClass: {
        stage: null,
        location: null,
        classNumber: null
      },
      classData: [false, []]
    }
  }
}
</script>

<style scoped>
div {
  padding: 10px;
}
.gugi-30 {
  font-family: 'Gugi', cursive;
  font-size: 30px;
}
.nanumG {
  font-family: 'Nanum Gothic', sans-serif;
}
.jua {
  font-family: 'Jua', sans-serif;
}
</style>
