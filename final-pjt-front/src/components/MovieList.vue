<template>
  <div>
    <Splide
      :options="{
        perPage: 5,
        heightRatio: 0.3,
        gap: 20,
        cover: true,
        isNavigation: true,
      }"
    >
      <movie-item
        v-for="movie in recommendMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </Splide>
    <hr />
    <Splide
      :options="{
        perPage: 5,
        heightRatio: 0.3,
        gap: 20,
        cover: true,
        isNavigation: true,
      }"
    >
      <movie-item
        v-for="movie in popularMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </Splide>
    <hr />
    <Splide
      :options="{
        perPage: 5,
        heightRatio: 0.3,
        gap: 20,
        cover: true,
        isNavigation: true,
      }"
    >
      <movie-item
        v-for="movie in scoreMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </Splide>
    <hr />
    <Splide
      :options="{
        perPage: 5,
        heightRatio: 0.3,
        gap: 20,
        cover: true,
        isNavigation: true,
      }"
    >
      <movie-item
        v-for="movie in releasedMovies"
        :key="movie.tmdb_id"
        :movie="movie"
      ></movie-item>
    </Splide>
  </div>
</template>

<script>
import MovieItem from "@/components/MovieItem";
import axios from "axios";
import { mapState } from "vuex";
import { Splide } from "@splidejs/vue-splide";
import "@splidejs/splide/dist/css/splide.min.css";

export default {
  name: "MovieList",
  components: {
    MovieItem,
    Splide,
  },
  data: function () {
    return {};
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