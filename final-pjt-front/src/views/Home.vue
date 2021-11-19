<template>
  <div class="home">
    <movie-list></movie-list>
    <!-- <movie-list-popular></movie-list-popular>
    <hr />
    <movie-list-recommend></movie-list-recommend>
    <hr />
    <movie-list-release></movie-list-release>
    <hr />
    <movie-list-score></movie-list-score> -->
  </div>
</template>

<script>
import MovieList from "@/components/MovieList";
// import MovieListPopular from "@/components/MovieListPopular";
// import MovieListRecommend from "@/components/MovieListRecommend";
// import MovieListRelease from "@/components/MovieListRelease";
// import MovieListScore from "@/components/MovieListScore";

export default {
  name: "Home",
  components: {
    MovieList,
    // MovieListPopular,
    // MovieListRecommend,
    // MovieListRelease,
    // MovieListScore,
  },
};
</script>
