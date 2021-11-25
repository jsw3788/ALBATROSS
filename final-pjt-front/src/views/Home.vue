<template>
  <div class="home">
    <movie-list></movie-list>
  </div>
</template>

<script>
import MovieList from "@/components/MovieList";

export default {
  name: "Home",
  components: {
    MovieList,
  },
};
</script>
