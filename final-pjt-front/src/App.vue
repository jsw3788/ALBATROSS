<template>
  <div id="app">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#">NavBar</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item><router-link to="/home">Home</router-link></b-nav-item>
            <b-nav-item
              ><router-link to="/people">People</router-link></b-nav-item
            >
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

            <div v-if="this.isLogin" class="d-flex">
              <div>
                <router-link @click.native="logout" to="#"
                  ><b-button>Logout</b-button>
                </router-link>
              </div>
              <div>
                <b-button @click="goToProfile">My profile</b-button>
              </div>
            </div>
            <div v-else>
              <b-button v-b-modal.signup-modal>Signup</b-button>
              <b-modal id="signup-modal"><signup-form></signup-form></b-modal>
              <b-button v-b-modal.login-modal>Login</b-button>
              <b-modal id="login-modal"><login-form></login-form></b-modal>
            </div>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <router-view class="container" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import SignupForm from "@/components/SignupForm";
import LoginForm from "@/components/LoginForm";
import { mapGetters } from "vuex";

export default {
  name: "App",
  // data: function () {
  //   return {
  //     isLogin: false,
  //   };
  // },
  components: {
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
    goToProfile: function () {
      // console.log(this.username)
      this.$router.push({
        name: "Profile",
        params: { username: this.username },
      });
    },
  },
  computed: {
    ...mapGetters(["isLogin"]),
    ...mapState(["username"]),
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background-color: #2c3e50;
}
</style>
