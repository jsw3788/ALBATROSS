<template>
  <div id="app" style="z-index: 5">
    <notifications group="auth_notify" />
    <notifications group="movie_notify" />
    <notifications group="review_notify" />
    <b-navbar
      toggleable="lg"
      type="dark"
      class="d-flex justify-content-even"
      style="background-color: #151515"
    >
      <div class="container d-flex justify-content-even">
        <b-navbar-brand href="#" class="mx-3"
          ><img
            src="@/assets/ALBATROSS (5).png"
            alt="albatross"
            style="height: 40px"
        /></b-navbar-brand>

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
              <div>
                <router-link @click.native="logout" to="#">
                  <b-button size="sm" class="mx-2"
                    ><i class="fas fa-sign-out-alt"></i
                  ></b-button>
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
                <b-button size="sm" v-b-modal.login-modal
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

    <router-view class="container" />

    <div class="container sticky-bottom">
      <footer
        class="
          d-flex
          flex-wrap
          justify-content-between
          align-items-center
          py-3
          mt-4
          border-top
        "
      >
        <div class="col-md-4 d-flex align-items-center">
          <a
            href="/"
            class="mb-3 me-2 mb-md-0 text-muted text-decoration-none lh-1"
          >
            <svg class="bi" width="30" height="24">
              <use xlink:href="#bootstrap"></use>
            </svg>
          </a>
          <span class="text-muted">© 2021 Albatross Company</span>
        </div>

        <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
          <li class="ms-3">
            <a class="text-muted" href="#"><i class="fab fa-gitlab"></i></a>
          </li>
        </ul>
      </footer>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import SignupForm from "@/components/authform/SignupForm";
import LoginForm from "@/components/authform/LoginForm";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "App",
  components: {
    SearchBar,
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
    goToMyProfile: function () {
      // console.log(this.username)
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
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/all/`,
    }).then((res) => {
      this.$store.dispatch("getAllMovies", res.data);
    });
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/`,
    })
      .then((res) => {
        this.$store.dispatch("getScoreMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/release_date/`,
    })
      .then((res) => {
        this.$store.dispatch("getReleasedMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/popularity/`,
    })
      .then((res) => {
        this.$store.dispatch("getPopularMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/recommend/`,
      headers: this.$store.getters.config,
    })
      .then((res) => {
        this.$store.dispatch("getRecommendMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  },
  computed: {
    ...mapGetters(["isLogin"]),
    ...mapState(["username"]),
  },
};
</script>


<style>
@font-face {
  font-family: "GowunDodum-Regular";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
#app {
  font-family: GowunDodum-Regular, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  min-height: 120vh;
  background-color: #3c415c;
  color: #d5d5d5;
}
footer {
  background-color: #3c415c;
}
</style>
