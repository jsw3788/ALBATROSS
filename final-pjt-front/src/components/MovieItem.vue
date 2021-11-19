<template>
  <div class="border-solid">
    <div @click="goDetailInfo">
      <p>{{ movie.title }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "MovieItem",
  props: {
    movie: Object,
  },
  methods: {
    goDetailInfo: function () {
      console.log(this.movie);
      this.$router.push({
        name: "Detail",
        params: {
          movie_id: this.movie.id,
        },
      });
    },
  },
};
</script>

<style>
</style>