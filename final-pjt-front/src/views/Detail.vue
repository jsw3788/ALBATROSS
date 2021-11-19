<template>
  <div>
    <p>{{ movie.title }}</p>
    <img :src="movie.poster_path" alt="" />
    <div>
      <review-form :movieId="movie.id"></review-form>
      <review-list :movieId="movie.id"></review-list>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ReviewForm from "@/components/review/ReviewForm";
import ReviewList from "@/components/review/ReviewList";

export default {
  name: "Detail",
  components: {
    ReviewForm,
    ReviewList,
  },
  data: function () {
    return {
      movie: "",
      reviews: "",
    };
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/detail/${this.$route.params.movie_id}`,
    })
      .then((res) => {
        console.log(res);
        this.movie = res.data;
      })
      .then({})
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/${this.$route.params.movie_id}/reviews/`,
    })
      .then((res) => {
        console.log(res);
        this.reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style>
</style>