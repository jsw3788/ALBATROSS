<template>
  <div>
    <div class="d-flex">
      <movie-item
        v-for="movie in popularMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
    <hr />
    <div class="d-flex">
      <movie-item
        v-for="movie in recommendMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
    <hr />
    <div class="d-flex">
      <movie-item
        v-for="movie in releasedMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
    <hr />
    <div class="d-flex">
      <movie-item
        v-for="movie in scoreMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
  </div>
</template>

<script>
import MovieItem from "@/components/MovieItem";
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "MovieList",
  components: {
    MovieItem,
  },
  computed: {
    ...mapState([
      "popularMovies",
      "recommendMovies",
      "releasedMovies",
      "scoreMovies",
    ]),
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/popularity/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.$store.dispatch("getPopularMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/popularity/`,
      // headers: this.setToken(),
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
      // headers: this.setToken(),
    })
      .then((res) => {
        this.$store.dispatch("getRecommendMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/release_date/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.$store.dispatch("getReleasedMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        this.$store.dispatch("getScoreMovies", res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style>
</style>