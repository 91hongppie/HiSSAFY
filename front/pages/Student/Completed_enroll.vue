<template>
  <div class="container">
    <h2 class="text-center">
      등록이 완료되었습니다.
    </h2>
    <img src="/assets/emojis/smiling.png" alt="Smiling Face">
  </div>
</template>

<script>
export default {
  method: {
    move () {
      this.$routes.push('/')
      setTimeout(this.move, 1000)
    }
  }
}
</script>

<style>

</style>
