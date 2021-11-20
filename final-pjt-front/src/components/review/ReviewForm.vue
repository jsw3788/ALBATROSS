<template>
  <div>
    <input type="text" v-model.trim="newReview" @keyup.enter="writeReview" />
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
        headers: this.$store.getters.config,
        data: {
          content: this.newReview,
        },
      })
        .then((res) => {
          this.$emit("add-review", res.data);
          this.newReview = null;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>