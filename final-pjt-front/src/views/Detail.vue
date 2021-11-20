<template>
  <div>
    <p>{{ movie.title }}</p>
    <img :src="movie.poster_path" alt="" />
    <div>
      <review-form :movieId="movie.id"></review-form>
      <review-list :movieId="movie.id"></review-list>
    </div>
    <div v-if="isLogin">
      <button v-if="wanted" @click="updatedWanted">
        보고싶어요 취소
      </button>
      <button v-else @click="updatedWanted">
        보고싶어요
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ReviewForm from "@/components/review/ReviewForm";
import ReviewList from "@/components/review/ReviewList";
import { mapGetters } from 'vuex'

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
      wanted: null,
      score: null,
    };
  },
  methods: {
    updatedWanted: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/wanted/${this.$route.params.movie_id}/`,
        headers: this.config,
      })
      .then((res) => {
        console.log(res);
        this.wanted = res.data.wanted
      })
      .catch((err) => {
        console.log(err);
      })
    },
    checkWanted: function () {
      axios({
        method: "get",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/wanted/${this.$route.params.movie_id}/`,
        headers: this.config,
      })
      .then((res) => {
        this.wanted = res.data.wanted
      })
      .catch((err) => {
        console.log(err);
      })
    },
    checkScore: function () {

    }

  },
  computed: {
    ...mapGetters([
      'isLogin',
      'config'
    ])
  },
  
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/detail/${this.$route.params.movie_id}`,
    })
      .then((res) => {
        // console.log(res);
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

    if(this.isLogin){
      this.checkWanted()
      this.checkScore()
    }
  },
};
</script>

<style>
</style>