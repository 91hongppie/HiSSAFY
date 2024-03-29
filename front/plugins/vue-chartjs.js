import Vue from 'vue'
import { Line, Doughnut, Bar } from 'vue-chartjs'

Vue.component('my-line', {
  extends: Line,
  props: {
    data: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    },
    location: {
      type: Number,
      default: 1
    }
  },
  updated () {
    this.renderChart(this.data, this.options)
  }
})

Vue.component('my-doughnut', {
  extends: Doughnut,
  props: {
    data: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    },
    location: {
      type: Number,
      default: 1
    }
  },
  watch: {
    location () {
      this.renderChart(this.data, this.options)
    }
  },
  mounted () {
    this.renderChart(this.data, this.options)
  }
})

Vue.component('my-bar', {
  extends: Bar,
  props: {
    data: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  },
  mounted () {
    this.renderChart(this.data, this.options)
  }
})
