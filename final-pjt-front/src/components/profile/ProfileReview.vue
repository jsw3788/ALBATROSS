<template>
  <div>
    <ul>
      <h3>리뷰 좋아요순</h3>
      <profile-review-item
        v-for="review in popular_reviews"
        :key="review.id"
        :review="review"
      >
      </profile-review-item>
    </ul>
    <ul>
      <h3>리뷰 작성일순</h3>
      <profile-review-item
        v-for="review in recent_reviews"
        :key="review.id"
        :review="review"
      >
      </profile-review-item>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import ProfileReviewItem from "@/components/profile/ProfileReviewItem";
import { mapState } from "vuex";

export default {
  name: "ProfileReview",
  components: {
    ProfileReviewItem,
  },
  props: {
    person: String,
  },
  data: function () {
    return {
      // 이 두 리스트는 형태가 같아야함
      popular_reviews: null,
      recent_reviews: null,
    };
  },
  created: function () {
    axios({
      method: "get",

      url: `http://127.0.0.1:8000/api/v1/${this.person}/reviews/popular/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        console.log("popular_reviews");
        console.log(res);
        this.popular_reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",

      url: `http://127.0.0.1:8000/api/v1/${this.person}/reviews/recent/`,
      // headers: this.setToken(),
    })
      .then((res) => {
        console.log("recent_reviews");
        console.log(res);
        this.recent_reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  computed: {
    ...mapState(["username"]),
  },
};
</script>

<style>
</style>