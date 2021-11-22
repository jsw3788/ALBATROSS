<template>
  <div>
    <div @click="goToDetail">
      {{ review.user }}
      {{ review.movie }}
      {{ review.content }}
      {{ review.created_at }}
      {{ review.updated_at }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileReviewItem",
  props: {
    review: Object,
  },
  methods: {
    goToDetail: function () {
      // this.$router.push({ name: 'ReviewDetail' , params: { review_id: this.review.id } })
    },
  },
};
</script>

<style>
</style>