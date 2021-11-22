<template>
  <div>
    <h3>Login</h3>
    <hr />
    <div class="mb-3">
      <label for="username">아이디</label>
      <input
        type="text"
        id="username"
        class="form-control"
        v-model="credentials.username"
      />
    </div>
    <div class="mb-3">
      <label for="password">비밀번호</label>
      <input
        type="password"
        id="password"
        class="form-control"
        v-model="credentials.password"
        @keyup.enter="login"
      />
    </div>
    <div class="d-flex justify-content-end">
      <b-button @click="login">로그인</b-button>
    </div>
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
      this.$store.dispatch("setUsername", this.credentials.username);
      this.$store.dispatch("login", this.credentials);
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
