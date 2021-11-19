<template>
  <div></div>
</template>

<script>
import axios from "axios";

export default {
  name: "Detail",
  data: function () {
    return { movie: null };
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/detail/${this.$route.params.movie_id}`,
    })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style>
</style>