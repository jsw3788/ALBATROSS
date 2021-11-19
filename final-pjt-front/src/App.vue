<template>
  <div id="app">
    <div id="nav">
      <router-link to="/home">Home</router-link> |
      <router-link to="/people">People</router-link>
    </div>
    <div v-if="this.isLogin">
      <router-link @click.native="logout" to="#"
        ><b-button>Logout</b-button>
      </router-link>
    </div>
    <div v-else>
      <!-- The modal -->
      <b-button v-b-modal.signup-modal>Signup</b-button>
      <b-modal id="signup-modal"><signup-form></signup-form></b-modal>
      <b-button v-b-modal.login-modal>Login</b-button>
      <b-modal id="login-modal"><login-form></login-form></b-modal>
    </div>
    <router-view />
  </div>
</template>

<script>
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
  },
  computed: {
    ...mapGetters(["isLogin"]),
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
