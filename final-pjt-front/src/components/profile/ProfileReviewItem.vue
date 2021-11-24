<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="3" class="mb-3">
          <img
            :src="nowmovie.poster_path"
            alt=""
            style="width: 100%"
            @click="goToDetail"
          />
        </b-col>
        <b-col cols="9">
          <div>
            {{ nowmovie.title }}
            {{ review.like_users }}
            <p class="text-start">{{ review.content }}</p>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "ProfileReviewItem",
  props: {
    review: Object,
  },
  methods: {
    goToDetail: function () {
      this.$router.push({
        name: "Detail",
        params: { movie_id: this.nowmovie.id },
      });
    },
  },
  computed: {
    ...mapState(["allmovies"]),
    nowmovie: function () {
      return this.allmovies[this.review.movie];
    },
  },
};
</script>

<style>
</style>