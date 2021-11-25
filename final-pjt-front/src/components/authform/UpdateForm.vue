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
        v-model="updateUsername"
      />
    </div>
    <div class="mb-3">
      <label for="update-password">비밀번호</label>
      <input
        type="password"
        id="update-password"
        class="form-control"
        v-model="password"
      />
    </div>
    <div class="mb-3">
      <label for="update-password-confirmation">비밀번호 확인</label>
      <input
        type="password"
        id="update-password-confirmation"
        class="form-control"
        v-model="passwordConfirmation"
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
    <div><b-button @click="deleteFile">프로필 이미지 삭제</b-button></div>
    <div class="d-flex justify-content-end">
      <b-button @click="updateProfile()">수정</b-button>
    </div>
  </div>
</template>

<script>
// import Vue from "vue";
// import axios from "axios";
import { mapState } from "vuex";
import { mapGetters } from "vuex";

export default {
  name: "UpdateForm",
  data: function () {
    return {
      updateUsername: this.username,
      password: null,
      passwordConfirmation: null,
      profileImg: this.profileImg,
    };
  },
  methods: {
    changeFile: function (event) {
      let file = event.target.files[0];
      this.profileImg = file;
    },
    deleteFile: function () {
      this.profileImg = "";
    },
    updateProfile: function () {
      console.log(this.updateUsername);
      console.log(this.passwordConfirmation);
      console.log(this.password);
      let profileData = new FormData();
      profileData.append("profileImg", this.profileImg);
      profileData.append("username", this.updateUsername);
      profileData.append("password", this.password);
      profileData.append("passwordConfirmation", this.passwordConfirmation);
      this.$store.dispatch("setProfileImg", profileData);
    },
  },
  computed: {
    ...mapState(["username, profileImg"]),
    ...mapGetters(["config"]),
  },
};
</script>

<style scoped>
</style>