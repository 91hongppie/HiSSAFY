<template>
  <v-app>
    <div class="navbar">
      <nav>
        <v-btn to="/" text class="title white--text"><span class="display-2"><span class="ssafy-blue">HI</span>SSAFY</span></v-btn>
        <span class="menu">
          <v-btn to="/main" text class="menu-button white--text title">대시보드</v-btn>
          <v-btn to="/main/classes" text class="menu-button white--text title">반별 현황</v-btn>
          <v-btn to="/main/students" text class="menu-button white--text title">개인별 현황</v-btn>
        </span>
      </nav>
      <section>
        <nuxt />
      </section>
    </div>
  </v-app>
</template>

<script>
export default {

}
</script>

<style scoped>
html, body, div {
  width: 100%; height: 100%;
  background-color: white;
}
nav {
  width: 20%; height: 100%;
  color: white;
  background: black;

  position: fixed;
  left: 0;
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: space-around;
}
section {
  margin-left: 20%;
  width: 100%; height: 100%;
  display: inline-block;
}
.navbar {
  display: flex;
}
.ssafy-blue {
  color: #3396F4;
}
.menu {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
}
.menu-button {
  display: block;
  margin-bottom: 20%;
}
.title {
  text-align: center;
  font-size: 40px;
}
</style>
