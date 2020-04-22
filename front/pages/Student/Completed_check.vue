<template>
  <v-container class="container blue">
    <h2 class="msg text-center">
      확인이 완료되었습니다.
    </h2>
    <div class="image text-center">
      <img class="face" src="../../assets/emojis/smiling.png" alt="Smiling Face">
    </div>
  </v-container>
</template>

<script>
export default {
  methods: {
    move () {
      setTimeout(this.$router.push('/'), 1000)
    }
  }
}

</script>

<style scoped>
.msg {
  font-size: 60pt;
  color: #ffffff;
}

.face {
  width: 400px;
  height: 400px;
}
</style>
