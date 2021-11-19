<template>
  <div id="movie-list-recommend">
    <h1>score</h1>
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
  name: "MovieListScore",
  components: {
    MovieItem,
  },
  computed: {
    ...mapState(["scoreMovies"]),
  },
  created: function () {
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