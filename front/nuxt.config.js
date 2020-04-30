
export default {
  mode: 'spa',
  loadingIndicator: {
    name: 'folding-cube',
    color: '#000',
    background: 'rgba(255,255,255,0.12)'
  },
  /*
  ** Headers of the page
  */
  head: {
    title: 'HI SSAFY!',
    // title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/hi_ssafy.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Gugi|Nanum+Gothic|Noto+Sans+KR|Jua&display=swap' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { 
    color: '#47c3d1',
    height: '7px'
  },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~plugins/vue-js-modal.js',
    { src: '~plugins/vue-chartjs.js', mode: 'client' }
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    '@nuxtjs/vuetify'
  ],
  vuetify: {
    /* module options */
  },
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: process.env.BASE_URL || 'https://i02b106.p.ssafy.io'
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
      config.node = {
        fs: 'empty'
      }
      return config
    }
  }
}
