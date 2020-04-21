<template>
  <v-app>
    <div class="navbar">
      <nav>
        <v-btn to="/" text class="title white--text"><span class="ssafy-blue">HI</span>SSAFY</v-btn>
        <span class="menu">
          <v-btn to="/main" text class="menu-button white--text">대시보드</v-btn>
          <v-btn to="/main/class" text class="menu-button white--text">반별 현황</v-btn>
          <v-btn text class="menu-button white--text">MENU</v-btn>
        </span>
        <span class="menu2">
          <v-btn text class="menu-button white--text">MENU</v-btn>
          <v-btn text class="menu-button white--text">MENU</v-btn>
        </span>
      </nav>
      <section>
        <nuxt class="nBody" />
      </section>
    </div>
  </v-app>
</template>

<script>
export default {

}
</script>

<style>
html, body, div {
  width: 100%; height: 100%;
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
  width: 100%; height: 100%;
  display: inline-block;
}
.navbar {
  display: flex;
}
.nBody {
  margin-left: 20%;
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
.menu2 {
  font-size: 20px;

  display: flex;
  justify-content: space-around;
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
