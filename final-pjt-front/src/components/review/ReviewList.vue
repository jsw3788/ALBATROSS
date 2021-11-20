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
    </div>
  </div>
</template>

<script>
export default {
  name: "reviewList",
  props: {
    review: Object,
  },
};
</script>

<style>
</style>