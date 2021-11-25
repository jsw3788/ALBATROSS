<template>
  <div id="NavBar">
    <div>
      <b-navbar
        toggleable="lg"
        type="dark"
        class="d-flex justify-content-even"
        style="background-color: #151515"
      >
        <div class="container d-flex justify-content-even">
          <b-navbar-brand class="mx-3">
            <router-link
              to="/"
              class="text-decoration-none"
              style="color: white"
              ><img
                src="@/assets/ALBATROSS (5).png"
                alt="albatross"
                style="height: 40px"
            /></router-link>
          </b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
              <div>
                <div class="d-flex justify-content-center align-items-between">
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
                </div>
              </div>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ms-auto align-items-center">
              <div>
                <b-nav-item>
                  <div>
                    <i class="fas fa-search mx-2"></i>
                    <search-bar></search-bar>
                  </div>
                </b-nav-item>
              </div>

              <div v-if="this.isLogin" class="d-flex justify-content-center">
                <div class="ms-2">
                  <router-link @click.native="logout" to="#">
                    <b-button size="sm" class="mx-2" variant="outline-secondary"
                      ><i class="fas fa-sign-out-alt"></i
                    ></b-button>
                  </router-link>
                </div>
                <div class="ms-2">
                  <b-button
                    size="sm"
                    @click="goToMyProfile"
                    class="mx-2"
                    variant="outline-secondary"
                  >
                    <i class="fas fa-user-circle"></i>
                  </b-button>
                </div>
              </div>
              <div v-else class="d-flex justify-content-center">
                <div class="ms-2">
                  <b-button
                    size="sm"
                    class="mx-2"
                    variant="outline-secondary"
                    v-b-modal.signup-modal
                    >signup</b-button
                  >
                  <b-modal id="signup-modal" hide-footer hide-header>
                    <signup-form></signup-form>
                  </b-modal>
                </div>
                <div class="ms-2">
                  <b-button
                    size="sm"
                    class="mx-2"
                    variant="outline-secondary"
                    v-b-modal.login-modal
                    ><i class="fas fa-sign-in-alt"></i>
                  </b-button>
                  <b-modal id="login-modal" hide-footer hide-header>
                    <login-form></login-form>
                  </b-modal>
                </div>
              </div>
            </b-navbar-nav>
          </b-collapse>
        </div>
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
      if (this.isLogin) {
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