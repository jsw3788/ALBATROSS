<template>
  <div id="review-list">
    <!-- 리뷰 하나당 대댓글이 다 달려야함 -->
    <!-- 댓글 -->
    <div>
      <div>
        <p>작성자 : {{ review.user.username }}</p>
      </div>
      <div>
        <p>{{ review.content }}</p>
        <p>{{ review.created_at }}</p>
        <p>{{ review.updated_at }}</p>
      </div>
      <div v-if="review.user.username === this.username">
        <button @click="updateReview">수정</button>
        <button @click="deleteReview">삭제</button>
      </div>
    </div>
    <!-- comment -->
    <div>
      <!-- comment form -->
      <input
        type="text"
        v-model.trim="newComment"
        @keyup.enter="writeComment"
      />
      <input type="checkbox" id="comment-spoil" v-model="newCommentSpoil" />
      <label for="comment-spoil">스포일러</label>
      <button @click="writeComment">댓글쓰기</button>
      <!-- comment list -->
      <review-comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @update-comment="updateComment"
        @delete-comment="deleteComment"
      ></review-comment>
    </div>
    <hr />
  </div>
</template>

<script>
import axios from "axios";
import ReviewComment from "@/components/review/ReviewComment";
import { mapState } from "vuex";

export default {
  name: "reviewList",
  components: {
    ReviewComment,
  },
  data: function () {
    return {
      newComment: null,
      newCommentSpoil: false,
      comments: "",
    };
  },
  props: {
    review: Object,
  },
  methods: {
    updateReview: function () {

    },
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
    writeComment: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/comments/`,
        headers: this.$store.getters.config,
        data: {
          content: this.newComment,
          is_spoiled: this.newCommentSpoil,
        },
      })
        .then((res) => {
          this.comments.push(res.data);
          this.newComment = null;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    updateComment: function (updatedcomment, beforecomment) {
      this.comments = this.comments.map(comment => {
        if (comment===updatedcomment){
          return updatedcomment
          }else{
            return comment
          }
        }
      )
      const idx = this.comments.indexOf(beforecomment)
      this.comments[idx] = updatedcomment
    },


    deleteComment: function (delComment) {
      const idx = this.comments.indexOf(delComment);
      this.comments.splice(idx, 1);
    },
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/`,
      headers: this.$store.getters.config,
    })
      .then(() => {
        // console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
    // 댓글 불러오기
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/comments`,
      headers: this.$store.getters.config,
    })
      .then((res) => {
        // console.log(res);
        this.comments = res.data;
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