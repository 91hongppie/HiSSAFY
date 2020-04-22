<template>
  <v-container class="container justify-center" onload="move()">
    <h2 class="msg text-center">
      등록이 완료되었습니다.
    </h2>
    <div class="image text-center">
      <img class="smiling" src="../../assets/emojis/smiling.png" alt="Smiling Face">
    </div>
  </v-container>
</template>

<script>
export default {
  created () {
    this.move()
  },
  method: {
    move () {
      this.$routes.push('/')
      setTimeout(1000)
    }
  }
}
</script>

<style>
.msg {
  font-size: 60pt;
  color: #ffffff;
}

.smiling {
  width: 400px;
  height: 400px;
}
</style>
