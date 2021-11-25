<template>
  <div
    id="review-from"
    class="d-flex justify-content-between align-items-center"
  >
    <div>{{ username }}</div>
    <div>
      <textarea
        v-model.trim="newReview"
        rows="1"
        class="form-control"
        @keyup.enter="writeReview"
        style="width: 200%"
      ></textarea>
    </div>
    <div class="d-flex align-items-center">
      <input
        type="checkbox"
        id="spoiler"
        v-model="newReviewSpoil"
        class="me-1"
      />
      <label for="spoiler" class="me-4">spoiler</label>
      <a href="" style="color: white" class="me-4" @click="writeReview"
        ><b-icon-pencil-square scale="2"></b-icon-pencil-square
      ></a>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

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
          this.newReviewSpoil = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  computed: {
    ...mapState(["username"]),
  },
};
</script>
