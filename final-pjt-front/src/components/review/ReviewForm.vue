<template>
  <div id="review-from">
    <div class="mx-5">
      <textarea
        v-model.trim="newReview"
        rows="3"
        class="form-control mb-2"
      ></textarea>
    </div>
    <div class="d-flex align-items-center justify-content-end">
      <input
        type="checkbox"
        id="spoiler"
        v-model="newReviewSpoil"
        class="m-2"
      />
      <label for="spoiler" class="me-2">spoiler</label>
      <a href="" style="color: white" @click="writeReview" class="mx-3 my-1"
        ><b-icon-pencil-square scale="2"></b-icon-pencil-square
      ></a>
    </div>
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
    writeReview: function (event) {
      event.preventDefault();
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
