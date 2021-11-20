<template>
  <div @click="goToDetail">
    {{ movie.poster_path }}
    {{ movie.title }}

  </div>
</template>

<script>
export default {
  name: 'ProfileMovieItem',
  props: {
    movie: Object,
  },
  methods: {
    goToDetail: function() {
      this.$router.push({ name: 'Detail' , params: { movie_id: this.movie.id } })
    }

  }

}
</script>

<style>

</style>