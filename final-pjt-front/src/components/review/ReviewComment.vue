<template>
  <div>
    <p>
      댓글 // {{ comment.user.username }} : {{ comment.content }} |
      {{ comment.id }}
      <span v-if="comment.user.username === this.username">
        <b-button v-b-modal="comment.id">수정</b-button>

        <b-modal :id="comment.id" title="BootstrapVue">
          <p class="my-4">Hello from modal!</p>
        </b-modal>
        <b-button @click="deleteComment">삭제</b-button>
      </span>
    </p>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "ReviewComment",
  props: {
    comment: Object,
  },
  data: function () {
    return { commentId: this.comment.id };
  },
  methods: {
    deleteComment: function () {
      const delComment = this.comment;
      axios({
        method: "delete",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/comments/${this.comment.id}/`,
        headers: this.$store.getters.config,
      }).then(() => {
        this.$emit("delete-comment", delComment);
      });
    },
  },
  computed: {
    ...mapState(["username"]),
  },
};
</script>

<style>
</style>