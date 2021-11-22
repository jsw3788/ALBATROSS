<template>
  <div id="signup">
    <h3>회원가입</h3>
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
      />
    </div>
    <div class="mb-3">
      <label for="password-confirmation">비밀번호 확인</label>
      <input
        type="password"
        id="password-confirmation"
        class="form-control"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      />
    </div>
    <div class="d-flex justify-content-end">
      <b-button @click="signup">회원가입</b-button>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
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
        .then(() => {
          this.$router.go();
        })
        .catch((err) => {
          Vue.notify({
            group: "auth_notify",
            title: "회원가입 실패",
            text: "이미 존재하는 계정이거나 비밀번호가 일치하지 않습니다!",
            type: "error",
          });
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
</style>