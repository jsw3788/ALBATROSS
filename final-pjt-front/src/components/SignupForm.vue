<template>
  <div id="signup">
    <h1>Signup</h1>
    <div>
      <label for="username">ID : </label>
      <input type="text" id="username" v-model="credentials.username" />
    </div>
    <div>
      <label for="password">PW : </label>
      <input type="password" id="password" v-model="credentials.password" />
    </div>
    <div>
      <label for="password-confirmation">PW : </label>
      <input
        type="password"
        id="password-confirmation"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      />
    </div>
    <button @click="signup">회원가입</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignupForm",
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
        passwordConfirmation: null,
      },
    };
  },
  methods: {
    signup: function () {
      axios({
        method: "post",
        // url: `${process.env.VUE_APP_SERVER_URL}/accounts/signup/`,
        url: `http://127.0.0.1:8000/api/v2/signup/`,
        data: this.credentials,
      })
        .then((res) => {
          console.log("확인");
          localStorage.setItem("jwt", res.data.token);
          // this.$emit("login")
          this.$router.go();
        })
        .catch((err) => {
          console.log("에러났어!");
          console.log(err);
        });
    },
  },
};
</script>