<template>
  <div class="border-solid">
    <p>{{ movie.title }}</p>
  </div>
</template>

<script>
export default {
  name: "MovieItem",
  props: {
    movie: Object,
  },
};
</script>

<style>
</style>