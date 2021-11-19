<template>
  <div id="movie-list-popular">
    <h1>popular</h1>
    <div class="d-flex">
      <movie-item
        v-for="movie in popularMovies"
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
  name: "MovieListPopular",
  components: {
    MovieItem,
  },
  computed: {
    ...mapState(["popularMovies"]),
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
  },
};
</script>

<style>
</style>