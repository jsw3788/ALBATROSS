<template>
  <SplideSlide class="movie-item">
    <div @click="goDetailInfo" class="movie-card">
      <img :src="movie.poster_path" style="width: 100%" />
    </div>
  </SplideSlide>
</template>

<script>
import { SplideSlide } from "@splidejs/vue-splide";
import "@splidejs/splide/dist/css/splide.min.css";

export default {
  name: "MovieItem",
  components: {
    SplideSlide,
  },
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
.movie-item {
  color: black;
}
/* .movie-card {
  object-fit: cover;
} */
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