<template>
  <div id="review-list">
    <div>
      <div>
        <p>작성자 : {{ review.user.username }}</p>
      </div>
      <div>
        <p>{{ review.content }}</p>
        <p>{{ review.created_at }}</p>
        <p>{{ review.updated_at }}</p>
      </div>
      <div>
        <button>수정</button>
        <button @click="deleteReview">삭제</button>
      </div>
    </div>
    <div></div>
    <hr />
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "reviewList",
  props: {
    review: Object,
  },
  methods: {
    deleteReview: function () {
      const delReview = this.review;
      axios({
        method: "delete",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/`,
        headers: this.$store.getters.config,
      }).then(() => {
        this.$emit("delete-review", delReview);
      });
    },
  },
};
</script>

<style>
</style>