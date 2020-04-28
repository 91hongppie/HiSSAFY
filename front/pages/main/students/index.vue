<template>
  <div>
    <div class="locationSelect d-flex justify-space-around align-center jua">
      <div>
        <v-combobox
          v-model="model"
          :items="locations"
          :search-input.sync="selectLo"
          hide-selected
          multiple
          chips
        >
          <template v-slot:selection="{ attrs, item, parent, selected }">
            <v-chip
              v-if="item === Object(item)"
              v-bind="attrs"
              color="blue lighten-1"
              :input-value="selected"
              label
            >
              <span class="pr-2" style="color: white;">
                {{ item.text }}
              </span>
              <v-icon
                small
                @click="parent.selectItem(item)"
              >mdi-close</v-icon>
            </v-chip>
          </template>
        </v-combobox>
      </div>
      <v-form class="d-flex justify-center align-center">
        <v-text-field v-model="searchName" placeholder="학생 이름"></v-text-field>
        <v-btn class="mx-3 selectButton">검색</v-btn>
      </v-form>
    </div>
    <div>
      <NuxtChild :key="searchName" />
    </div>
  </div>
</template>

<script>
export default {
  layout: 'super',
  data () {
    return {
      model: [],
      locations: [
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
        }
      ],
      selectLo: null,
      searchName: null
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
