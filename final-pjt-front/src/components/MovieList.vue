<template>
  <div>
    <slick ref="slick" :options="slickOptions">
      <movie-item
        v-for="movie in popularMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </slick>
    <hr />
    <div class="d-flex recommend-movie-list">
      <movie-item
        v-for="movie in recommendMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
    <hr />
    <div class="d-flex released-movie-list">
      <movie-item
        v-for="movie in releasedMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </div>
    <hr />
    <div class="d-flex score-movie-list">
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
import Slick from "vue-slick";
import "slick-carousel/slick/slick.css";

export default {
  name: "MovieList",
  components: {
    MovieItem,
    Slick,
  },
  data: function () {
    return {
      slickOptions: {
        slidesToShow: 5,
        shileToScroll: 5,
      },
    };
  },
  // methods: {
  //   next() {
  //     this.$refs.slick.next();
  //   },

  //   prev() {
  //     this.$refs.slick.prev();
  //   },
  // },
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
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/`,
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