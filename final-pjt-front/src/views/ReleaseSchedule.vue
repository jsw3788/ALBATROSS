<template>
  <v-calendar :attributes="attrs" />
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ReleaseSchedule",
  computed: {
    ...mapState(["allmovies"]),
    attrs() {
      console.log(this.allmovies);
      return [
        this.allmovies.map((movie) => ({
          dates: new Date(movie.release_date),
          bar: true,
        })),
      ];
    },
  },
  methods: {
    onClick: function () {
      console.log(new Date(this.allmovies[0].release_date));
      console.log(this.attributes);
    },
  },
};
</script>

<style>
</style>