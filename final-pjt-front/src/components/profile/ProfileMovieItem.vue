<template>
  <b-col cols="6" lg="3">
    <div @click="goToDetail">
      <img :src="movie.poster_path" style="width: 100%" />
      {{ movie.title }}
    </div>
  </b-col>
</template>

<script>
export default {
  name: "ProfileMovieItem",
  props: {
    movie: Object,
  },
  methods: {
    goToDetail: function () {
      this.$router.push({
        name: "Detail",
        params: { movie_id: this.movie.id },
      });
    },
  },
};
</script>

<style>
</style>