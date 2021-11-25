<template>
  <div id="review-from">
    <h4 class="text-start mb-4">Review</h4>
    <div class="d-flex align-items-center">
      <input
        v-model.trim="newReview"
        class="mx-3"
        @keyup.enter="writeReview"
        style="width: 100%"
        :disabled="isLogin == false"
      />
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
import { mapGetters, mapState } from "vuex";
import Vue from "vue";

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
        .catch(() => {
          Vue.notify({
            group: "review_notify",
            title: "멈춰!",
            text: "리뷰 작성을 위해 로그인이 필요합니다.",
            type: "warn",
            closeOnClick: true,
          });
        });
    },
  },
  computed: {
    ...mapState(["username", "profileImg"]),
    ...mapGetters(["isLogin"]),
  },
};
</script>
