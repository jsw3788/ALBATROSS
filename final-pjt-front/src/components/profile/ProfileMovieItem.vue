<template>
  <div @click="goToDetail">
    <img :src="movie.poster_path" alt="" />
    {{ movie.title }}
  </div>
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