<template>
  <div id="app">
    <notifications group="auth_notify" />
    <notifications group="movie_notify" />
    <notifications group="review_notify" />
    <div v-if="!isIndex">
      <b-navbar
        toggleable="lg"
        type="dark"
        variant="dark"
        class="d-flex justify-content-end"
        
      >
        <b-navbar-brand href="#"> <img src="@/assets/ALBATROSS.png" alt="albatross"> </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <div class="d-flex">
              <div>
                <b-nav-item>
                  <router-link to="/home" class="text-decoration-none"
                    >Home</router-link
                  >
                </b-nav-item>
              </div>
              <div>
                <b-nav-item>
                  <router-link to="/people" class="text-decoration-none"
                    >People</router-link
                  >
                </b-nav-item>
              </div>
            </div>
            <div>
              <b-nav-item>
                <div>
                  <i class="fas fa-search mx-2"></i>
                  <search-bar></search-bar>
                </div>
              </b-nav-item>
            </div>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <!-- <b-nav-form class="d-flex">
              <div>
                <b-form-input
                  size="sm"
                  class="mr-sm-2"
                  placeholder="Search"
                ></b-form-input>
              </div>
              <div>
                <b-button size="sm" class="my-2 my-sm-0" type="submit"
                  >Search</b-button
                >
              </div>
            </b-nav-form> -->

            <div v-if="this.isLogin" class="d-flex justify-content-center">
              <div>
                <router-link @click.native="logout" to="#">
                  <b-button size="sm" class="mx-2">Logout</b-button>
                </router-link>
              </div>
              <div>
                <b-button size="sm" @click="goToMyProfile" class="mx-2">{{
                  username
                }}</b-button>
              </div>
            </div>
            <div v-else class="d-flex justify-content-center">
              <div>
                <b-button size="sm" v-b-modal.signup-modal>Signup</b-button>
                <b-modal id="signup-modal" hide-footer hide-header>
                  <signup-form></signup-form>
                </b-modal>
              </div>
              <div>
                <b-button size="sm" v-b-modal.login-modal>Login</b-button>
                <b-modal id="login-modal" hide-footer hide-header>
                  <login-form></login-form>
                </b-modal>
              </div>
            </div>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <router-view class="container" />
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import SignupForm from "@/components/authform/SignupForm";
import LoginForm from "@/components/authform/LoginForm";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "App",
  components: {
    SearchBar,
    SignupForm,
    LoginForm,
  },
  // created: function () {
  //   const token = localStorage.getItem("jwt");
  //   if (token) {
  //     this.isLogin = true;
  //   }
  // },
  methods: {
    logout: function () {
      this.$store.dispatch("logout");

      // this.isLogin = false;
      // localStorage.removeItem("jwt");
      // this.$router.push({ name: "Home" });
    },
    goToMyProfile: function () {
      // console.log(this.username)
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
  created: function () {

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/all/`,
      headers: this.$store.getters.config,
    }).then((res) => {
      this.$store.dispatch("getAllMovies", res.data);
    });

    
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
  text-align: center;
  background-color: #14181c;
  color: white;
}
</style>
