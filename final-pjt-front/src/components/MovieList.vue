<template>
  <div>
    <h4 class="mt-5">인기영화</h4>
    <carousel
      :loop="true"
      :navigationClickTargetSize="25"
      :paginationSize="5"
      :navigationEnabled="true"
      :perPageCustom="[
        [576, 2],
        [768, 3],
        [992, 4],
        [1200, 5],
      ]"
      :paginationActiveColor="'#ff0000'"
      :paginationColor="'#ffffff'"
    >
      <slide v-for="movie in popularMovies" :key="movie.tmdb_id">
        <div @click="goDetailInfo(movie)" class="poster p-2">
          <img
            :src="movie.poster_path"
            class="poster-img"
            style="width: 100%"
          />
          <p class="poster-text">{{ movie.title }}</p>
        </div>
      </slide>
    </carousel>
    <h4 class="mt-5">추천영화</h4>
    <carousel
      :loop="true"
      :navigationClickTargetSize="25"
      :paginationSize="5"
      :navigationEnabled="true"
      :perPageCustom="[
        [576, 2],
        [768, 3],
        [992, 4],
        [1200, 5],
      ]"
      :paginationActiveColor="'#ff0000'"
      :paginationColor="'#ffffff'"
    >
      <slide v-for="movie in recommendMovies" :key="movie.tmdb_id">
        <div @click="goDetailInfo(movie)" class="poster p-2">
          <img
            :src="movie.poster_path"
            class="poster-img"
            style="width: 100%"
          />
          <p class="poster-text">{{ movie.title }}</p>
        </div>
      </slide>
    </carousel>
    <h4 class="mt-5">평점이 높은 영화</h4>
    <carousel
      :loop="true"
      :navigationClickTargetSize="25"
      :paginationSize="5"
      :navigationEnabled="true"
      :perPageCustom="[
        [576, 2],
        [768, 3],
        [992, 4],
        [1200, 5],
      ]"
      :paginationActiveColor="'#ff0000'"
      :paginationColor="'#ffffff'"
    >
      <slide v-for="movie in scoreMovies" :key="movie.tmdb_id">
        <div @click="goDetailInfo(movie)" class="poster p-2">
          <img
            :src="movie.poster_path"
            class="poster-img"
            style="width: 100%"
          />
          <p class="poster-text">{{ movie.title }}</p>
        </div>
      </slide>
    </carousel>
    <h4 class="mt-5">최신영화</h4>
    <carousel
      :loop="true"
      :navigationClickTargetSize="25"
      :paginationSize="5"
      :navigationEnabled="true"
      :perPageCustom="[
        [576, 2],
        [768, 3],
        [992, 4],
        [1200, 5],
      ]"
      :paginationActiveColor="'#ff0000'"
      :paginationColor="'#ffffff'"
    >
      <slide v-for="movie in releasedMovies" :key="movie.tmdb_id">
        <div @click="goDetailInfo(movie)" class="poster p-2">
          <img
            :src="movie.poster_path"
            class="poster-img"
            style="width: 100%"
          />
          <p class="poster-text">{{ movie.title }}</p>
        </div>
      </slide>
    </carousel>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Carousel, Slide } from "vue-carousel";

export default {
  name: "MovieList",
  components: {
    Carousel,
    Slide,
  },
  computed: {
    ...mapState([
      "popularMovies",
      "recommendMovies",
      "releasedMovies",
      "scoreMovies",
    ]),
  },
  methods: {
    goDetailInfo: function (movie) {
      this.$router.push({
        name: "Detail",
        params: {
          movie_id: movie.id,
        },
      });
    },
  },
};
</script>

<style scoped>
/* poster img hover_text */
/* 부모태그 poster 사진 poster-img 글 poster-text*/
.poster-img {
  vertical-align: top;
}
.poster {
  display: inline-block;
  position: relative;
}
.poster:hover:after,
.poster:hover > .poster-text {
  display: block;
}
.poster:after,
.poster-text {
  display: none;
}

.poster:after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 10;
}
.poster {
  overflow: hidden;
}
.poster .poster-img {
  height: 340px;
}
.poster:hover .poster-img {
  transform: scale(1.2);
  transition: 1s;
}
.poster-text {
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  top: 5%;
  color: #fff;
  z-index: 20;
  font-weight: 600;
  font-size: 20px;
}
</style>