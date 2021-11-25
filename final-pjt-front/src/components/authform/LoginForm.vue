<template>
  <div>
    <h3>로그인</h3>
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
    login: function () {
      this.$store.dispatch("login", this.credentials);
      this.$store.dispatch("setUsername", this.credentials.username);
    },
  },
};
</script>
