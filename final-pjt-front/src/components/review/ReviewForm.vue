<template>
  <div id="review-from">
    <input type="text" v-model.trim="newReview" @keyup.enter="writeReview" />
    <input type="checkbox" id="spoiler" v-model="newReviewSpoil" />
    <label for="spoiler">스포일러</label>
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
      newReviewSpoil: false,
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
          is_spoiled: this.newReviewSpoil,
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
