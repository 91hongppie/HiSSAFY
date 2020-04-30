<template>
  <div>
    <div class="locationSelect d-flex justify-space-around align-center jua">
      <v-form>
        <v-container>
          <v-row>
            <v-col cols="6" class="d-flex justify-center align-center" style="max-width: 100%;">
              <v-combobox
                v-model="model"
                :items="locations"
                placeholder="지역"
                hide-selected
                multiple
                chips
                height="40px"
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
            </v-col>
            <v-col cols="4" class="d-flex justify-center align-center">
              <v-text-field v-model="searchName" placeholder="학생 이름" height="40px"></v-text-field>
            </v-col>
            <v-col cols="2" class="d-flex justify-center align-center">
              <v-btn class="mx-3 selectButton" :to="`/main/students/${ joinParams() }`" height="40px">검색</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </div>
    <div>
      <NuxtChild :key="joinParams()" />
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
          text: '구미',
          value: 3
        },
        {
          text: '광주',
          value: 4
        }
      ],
      selectLo: [],
      searchName: null,
      urlParams: {}
    }
  },
  watch: {
    model: {
      deep: true,
      handler () {
        const temp = []
        for (const modelIndex in this.model) {
          temp.push(this.model[modelIndex].value)
        }
        this.selectLo = temp
      }
    }
  },
  methods: {
    joinParams () {
      let temp = ''
      if (this.selectLo.length > 0) {
        temp += `${this.selectLo.join('')}`
      }
      if (this.searchName !== null) {
        temp += `&${this.searchName}`
      }
      return temp
    }
    // getUrlParams () {
    //   const params = {}
    //   window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (str, key, value) { params[key] = value })
    //   return params
    // },
    // searchStudent () {
    //   this.urlParams = this.getUrlParams()
    //   console.log(this.urlParams)
    // }
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
