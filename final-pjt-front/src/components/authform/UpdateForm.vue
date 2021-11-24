<template>
  <div id="update">
    <h3>회원정보 수정</h3>
    <hr />
    <div class="mb-3">
      <label for="update-username">아이디</label>
      <input
        type="text"
        id="update-username"
        class="form-control"
        v-model="credentials.updateUsername"
      />
    </div>
    <div class="mb-3">
      <label for="update-password">비밀번호</label>
      <input
        type="password"
        id="update-password"
        class="form-control"
        v-model="credentials.password"
      />
    </div>
    <div class="mb-3">
      <label for="update-password-confirmation">비밀번호 확인</label>
      <input
        type="password"
        id="update-password-confirmation"
        class="form-control"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
      />
    </div>
    <div class="mb-3">
      <label for="profile-img">프로필 이미지</label>
      <input
        @change="changeFile"
        type="file"
        id="profile-img"
        class="form-control"
        accept="image/*"
      />
    </div>
    <div><button @click="deleteFile">프로필 이미지 삭제</button></div>
    <div class="d-flex justify-content-end">
      <b-button @click="updateProfile">수정</b-button>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import { mapState } from "vuex";
import { mapGetters } from "vuex";

export default {
  name: "UpdateForm",
  data: function () {
    return {
      credentials: {
        updateUsername: this.username,
        password: null,
        passwordConfirmation: null,
        profilePath: this.profileImg,
      },
    };
  },
  methods: {
    changeFile: function (event) {
      let file = event.target.files[0];
      this.credentials.profilePath = file;
    },
    deleteFile: function () {
      this.credentials.profilePath = "";
    },
    updateProfile: function () {
      console.log(this.username);
      axios({
        method: "put",
        url: `http://127.0.0.1:8000/api/v2/${this.username}/profile/`,
        data: this.credentials,
        headers: this.config,
      })
        .then(() => {
          this.$router.go();
        })
        .catch((err) => {
          Vue.notify({
            group: "auth_notify",
            title: "정보 수정 실패",
            text: "이미 존재하는 아이디거나, 비밀번호가 일치하지 않습니다!",
            type: "error",
          });
          console.log(err);
        });
    },
  },
  computed: {
    ...mapState(["username", "profileImg"]),
    ...mapGetters(["config"]),
  },
};
</script>

<style scoped>
</style>