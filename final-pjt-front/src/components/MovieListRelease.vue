<template>
  <div id="movie-list-released">
    <h1>released</h1>
    <div class="d-flex">
      <movie-item
        v-for="movie in releasedMovies"
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
  name: "MovieListRelease",
  components: {
    MovieItem,
  },
  computed: {
    ...mapState(["releasedMovies"]),
  },
  created: function () {
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
  },
};
</script>

<style>
</style>