<template>
  <div class="navbar">
    <nav>
      <a class="title"><span class="ssafy-blue">HI</span>SSAFY</a>
      <span class="menu">
        <a class="menu-button">MENU</a>
        <a class="menu-button">MENU</a>
        <a class="menu-button">MENU</a>
      </span>
      <span class="menu2">
        <a class="menu-button">MENU</a>
        <a class="menu-button">MENU</a>
      </span>
    </nav>
    <section>
      <nuxt />
    </section>
  </div>
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

  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: space-around;
}
section {
  width: 80%; height: 100%;
  display: inline-block;
}
.navbar {
  display: flex;
}
.ssafy-blue {
  color: #3396F4;
}
.menu {
  text-align: right;
  font-size: 30px;

  margin-right: 10%;
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
