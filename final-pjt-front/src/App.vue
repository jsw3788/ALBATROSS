<template>
  <div id="app">
    <notifications group="auth_notify" />
    <notifications group="movie_notify" />
    <notifications group="review_notify" />
    <nav-bar></nav-bar>
    <router-view class="container" />
    <footer-bar></footer-bar>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";
import FooterBar from "@/components/FooterBar";
import { mapGetters } from "vuex";
import { mapState } from "vuex";

export default {
  name: "App",
  components: {
    FooterBar,
    NavBar,
  },
  methods: {
    logout: function () {
      this.$store.dispatch("logout");
    },
    goToMyProfile: function () {
      if (this.username) {
        this.$router.push({
          name: "Profile",
          params: { username: this.username },
        });
      } else {
        alert("로그인을 해주세요");
      }
    },
  },
  computed: {
    ...mapGetters(["isLogin"]),
    ...mapState(["username"]),
  },
};
</script>


<style>
@font-face {
  font-family: "GowunDodum-Regular";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
#app {
  font-family: GowunDodum-Regular, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  z-index: 5;
  padding-bottom: 20vh;
  text-align: center;
  min-height: 120vh;
  background-color: #1f1d36;
  color: #d5d5d5;
}
footer {
  background-color: #1f1d36;
}
i {
  color: #d5d5d5;
}
</style>
