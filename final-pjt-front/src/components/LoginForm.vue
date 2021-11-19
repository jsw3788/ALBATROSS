<template>
  <div>
    <h1>Login</h1>
    <div>
      <label for="username">ID : </label>
      <input type="text" id="username" v-model="credentials.username" />
    </div>
    <div>
      <label for="password">PW : </label>
      <input
        type="password"
        id="password"
        v-model="credentials.password"
        @keyup.enter="login"
      />
    </div>
    <button @click="login">로그인</button>
  </div>
</template>

<script>
// import axios from "axios";
// import { mapActions } from "vuex";

export default {
  name: "Login",
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      },
    };
  },
  methods: {
    // ...mapActions(["login"]),
    login: function () {
      this.$store.dispatch("login", this.credentials);
      // this.$router.go();
    },
    // login: function () {
    //   axios({
    //     method: "post",
    //     url: `${process.env.VUE_APP_SERVER_URL}/api/v2/api-token-auth/`,
    //     data: this.credentials,
    //   })
    //     .then((res) => {
    //       console.log(res);
    //       localStorage.setItem("jwt", res.data.token);
    //       // this.$emit("login");
    //       this.$router.go();
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // },
  },
};
</script>
