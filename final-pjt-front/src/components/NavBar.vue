<template>
  <div id="NavBar">
    <div>
      <b-navbar
        toggleable="lg"
        type="dark"
        class="d-flex justify-content-end"
        style="background-color: #151515"
      >
        <b-navbar-brand href="#" class="mx-3">
          <img
            src="@/assets/ALBATROSS (5).png"
            alt="albatross"
            style="height: 40px"
          />
        </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <div>
              <div class="d-flex justify-content-center">
                <div class="mx-2">
                  <b-nav-item>
                    <router-link
                      to="/home"
                      class="text-decoration-none"
                      style="color: white"
                      ><b-icon-camera-reels></b-icon-camera-reels
                    ></router-link>
                  </b-nav-item>
                </div>
                <div class="mx-2">
                  <b-nav-item>
                    <router-link
                      to="/people"
                      class="text-decoration-none"
                      style="color: white"
                      ><b-icon-people></b-icon-people
                    ></router-link>
                  </b-nav-item>
                </div>
                <div class="mx-2">
                  <b-nav-item>
                    <router-link
                      to="/release"
                      class="text-decoration-none"
                      style="color: white"
                      >임시</router-link
                    >
                  </b-nav-item>
                </div>
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

          <b-navbar-nav class="ml-auto">
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
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import SignupForm from "@/components/authform/SignupForm";
import LoginForm from "@/components/authform/LoginForm";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
export default {
  name: "NavBar",
  components: {
    SearchBar,
    SignupForm,
    LoginForm,
  },
  methods: {
    logout: function () {
      this.$store.dispatch("logout");
    },
    goToMyProfile: function () {
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
  computed: {
    ...mapGetters(["isLogin"]),
    ...mapState(["username"]),
  },
};
</script>

<style>
</style>