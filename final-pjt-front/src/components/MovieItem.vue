<template>
  <div>
    <div @click="goDetailInfo">
      <b-card
        :img-src="movie.poster_path"
        img-alt="Image"
        img-top
        style="max-width: 20rem; font-size: 5px"
        class="mb-2 movie-card"
      >
        <p class="hover-title">{{ movie.title }}</p>
      </b-card>
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



<style scoped>
.movie-card:hover {
  filter: brightness(50%);
}
.movie-card:hover .hover-title {
  opacity: 1;
}
/* .hover-title {
  visibility: hidden;
} */
/* .movie-card:hover:after {
  display: block;
}
.movie-card:hover > .hover-title {
  display: block;
} */
</style>