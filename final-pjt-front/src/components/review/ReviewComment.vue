<template>
  <div>
    <p>
      댓글 // {{ comment.user.username }} : {{ comment.content }}
      <span v-if="comment.user.username === this.username">
        <b-button v-b-modal="'update'+comment.id">수정</b-button>

        <b-modal title="댓글 수정" :id="'update'+comment.id" ok-only hide-footer>
        <template #default="{ close }">
          <input
            type="text"
            v-model="updatedcontent"
            @keyup.enter="updateComment"  
          >
          <b-button @click="[updateComment(), close()]">수정</b-button>
        </template>
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
  data: function(){
    return {
      updatedcontent: this.comment.content
    }
  },
  methods: {
    updateComment: function () {
      axios({
        method:"put",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/comments/${this.comment.id}/`,
        headers: this.$store.getters.config,
        data: {
          content:this.updatedcontent
        }
      }).then(() => {
        const updatedcomment = {
          ...this.comment,
          content: this.updatedcontent
        }
        this.$emit("update-comment", updatedcomment, this.comment)
      })
    },
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