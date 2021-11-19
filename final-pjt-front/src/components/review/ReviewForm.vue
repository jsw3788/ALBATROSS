<template>
  <div>
    <input type="text" v-model="newReview" />
    <button @click="writeReview">작성</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ReviewForm",
  data: function () {
    return {
      newReview: null,
    };
  },
  props: {
    movieId: Number,
  },
  methods: {
    writeReview: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/${this.movieId}/reviews/`,
        params: {
          movie_pk: this.movieId,
        },
      });
    },
  },
};
</script>

<style>
</style>