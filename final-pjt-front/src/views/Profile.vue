<template>
  <b-container class="bv-example-row">
    <b-row class="mt-5">
      <b-col cols="4">
        <div style="position: fixed; width: 25%">
          <span>
            <img
              :src="image"
              alt="profile_image"
              style="width: 50%; border-radius: 50%"
              class="my-3"
            />
            <p>
              <span class="mx-1"> {{ person }}</span>
              <span v-if="isMySelf" class="mx-1">
                <b-button
                  size="sm"
                  v-b-modal.update-modal
                  variant="outline-secondary"
                  ><i class="fas fa-user-edit"></i
                ></b-button>
                <b-modal id="update-modal" hide-header ok-only>
                  <update-form></update-form>
                </b-modal>
              </span>
            </p>
          </span>
          <div>
            <p>films | {{ films }}</p>
            <p>follower | {{ follower }}</p>
            <p>following | {{ following }}</p>
          </div>
          <div v-if="!isMySelf">
            <button v-if="isfollowing" @click="follow">언팔로우</button>
            <button v-else @click="follow">팔로우</button>
          </div>
        </div>
      </b-col>
      <b-col cols="8">
        <b-container class="bv-example-row">
          <h4>가장 좋아하는 영화</h4>
          <b-row>
            <profile-movie-item
              v-for="(movie, index) in favorite_movies"
              :key="index + 'favorite'"
              :movie="movie"
            ></profile-movie-item>
          </b-row>
          <hr />
          <h4>최근 리뷰 영화</h4>
          <b-row>
            <profile-movie-item
              v-for="(movie, index) in recent_movies"
              :key="index + 'mrecent'"
              :movie="movie"
            >
            </profile-movie-item>
          </b-row>
          <hr />
          <h4>좋아요를 받이받은 리뷰</h4>
          <b-row>
            <profile-review-item
              v-for="(review, index) in popular_reviews"
              :key="index + 'popular'"
              :review="review"
            >
            </profile-review-item>
          </b-row>
          <hr />
          <h4>최근 작성한 리뷰</h4>
          <b-row>
            <profile-review-item
              v-for="(review, index) in recent_reviews"
              :key="index + 'rrecent'"
              :review="review"
            >
            </profile-review-item>
          </b-row>
        </b-container>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import ProfileMovieItem from "@/components/profile/ProfileMovieItem";
import ProfileReviewItem from "@/components/profile/ProfileReviewItem";
import UpdateForm from "@/components/authform/UpdateForm";
import { mapGetters } from "vuex";

export default {
  name: "Profile",
  components: {
    ProfileMovieItem,
    ProfileReviewItem,
    UpdateForm,
  },
  data: function () {
    return {
      person: null,
      follower: null,
      following: null,
      isfollowing: null,
      image: null,
      films: null,

      favorite_movies: null,
      recent_movies: null,
      popular_reviews: null,
      recent_reviews: null,
    };
  },
  methods: {
    follow: function () {
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/v2/${this.person}/follow/`,
        headers: this.config,
      }).then((res) => {
        this.isfollowing = res.data.following;
        this.follower = res.data.followingCnt;
        this.following = res.data.followerCnt;
      });
    },
  },
  created: function () {
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/api/v2/${this.$route.params.username}/profile/`,
      headers: this.config,
    })
      .then((res) => {
        this.person = res.data.username;
        this.isfollowing = res.data.following;
        this.following = res.data.followingCnt;
        this.follower = res.data.followerCnt;
        this.image =
          `${process.env.VUE_APP_SERVER_URL}/media/` + res.data.profile_image;
        this.films = res.data.movieCnt;
      })
      .catch((err) => {
        console.log(err);
      });
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/api/v1/${this.$route.params.username}/movies/favorite/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.favorite_movies = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/api/v1/${this.$route.params.username}/movies/recent/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        // console.log('recent_movies')
        // console.log(res)
        this.recent_movies = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
    axios({
      method: "get",

      url: `http://127.0.0.1:8000/api/v1/${this.$route.params.username}/reviews/popular/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.popular_reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",

      url: `http://127.0.0.1:8000/api/v1/${this.$route.params.username}/reviews/recent/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.recent_reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  computed: {
    isMySelf: function () {
      if (this.person != localStorage.getItem("username")) {
        return false;
      } else {
        return true;
      }
    },
    ...mapGetters(["config"]),
  },
};
</script>

<style>
</style>