<template>
  <div id="review-list">
    <!-- 리뷰 하나당 대댓글이 다 달려야함 -->
    <!-- 댓글 -->
    <div>
      <div>
        <p>
          작성자 : <span @click="goProfile">{{ review.user.username }}</span>
        </p>
      </div>
      <div>
        <p>{{ review.content }}</p>
        <p>{{ review.created_at }}</p>
        <p>{{ review.updated_at }}</p>
        <p>{{ commentCnt }}개의 댓글이 있습니다</p>
      </div>
      <div v-if="isLogin">
        <p>
          <span>{{ likeCnt }}</span>
          <i
            class="far fa-thumbs-up mx-2"
            style="color: rgb(0, 149, 246)"
            v-if="!isLiked"
            @click="like"
          >
          </i>
          <i
            class="fas fa-thumbs-up mx-2"
            style="color: rgb(0, 149, 246)"
            v-else
            @click="like"
          >
          </i>
          <span>{{ dislikeCnt }}</span>
          <i
            class="far fa-thumbs-down mx-2"
            style="color: rgb(0, 149, 246)"
            v-if="!isDisliked"
            @click="dislike"
          ></i>
          <i
            class="fas fa-thumbs-down mx-2"
            style="color: rgb(0, 149, 246)"
            v-else
            @click="dislike"
          ></i>
        </p>
      </div>

      <div v-if="review.user.username === this.username">
        <b-button v-b-modal="'update' + review.id">수정</b-button>
        <b-modal
          title="리뷰 수정"
          :id="'update' + review.id"
          ok-only
          hide-footer
        >
          <template #default="{ close }">
            <input
              type="text"
              v-model.trim="updatedcontent"
              @keyup.enter="updateReview"
            />
            <b-button @click="[updateReview(), close()]">수정</b-button>
          </template>
        </b-modal>
        <b-button @click="deleteReview">삭제</b-button>
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
import Vue from "vue";
import axios from "axios";
import ReviewComment from "@/components/review/ReviewComment";
import { mapState } from "vuex";
import { mapGetters } from "vuex";

export default {
  name: "reviewList",
  components: {
    ReviewComment,
  },
  data: function () {
    return {
      updatedcontent: this.review.content,
      newComment: null,
      newCommentSpoil: false,
      comments: "",
      isLiked: null,
      isDisliked: null,
      likeCnt: null,
      dislikeCnt: null,
      commentCnt: null,
    };
  },
  props: {
    review: Object,
  },
  methods: {
    like: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/likes/`,
        headers: this.$store.getters.config,
      })
        .then((res) => {
          this.isLiked = res.data.isLiked;
          this.likeCnt = res.data.likeCnt;
        })
        .catch(() => {
          Vue.notify({
            group: "review_notify",
            title: "앗!",
            text: "이미 비공감을 눌렀어요!",
            type: "warn",
          });
        });
    },
    dislike: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/dislikes/`,
        headers: this.$store.getters.config,
      })
        .then((res) => {
          this.isDisliked = res.data.isDisliked;
          this.dislikeCnt = res.data.dislikeCnt;
        })
        .catch(() => {
          Vue.notify({
            group: "review_notify",
            title: "앗!",
            text: "이미 공감을 눌렀어요!",
            type: "warn",
          });
        });
    },
    goProfile: function () {
      this.$router.push({
        name: "Profile",
        params: { username: this.review.user.username },
      });
    },
    updateReview: function () {
      axios({
        method: "put",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/`,
        headers: this.$store.getters.config,
        data: {
          content: this.updatedcontent,
        },
      }).then(() => {
        const updatedreview = {
          ...this.review,
          content: this.updatedcontent,
        };
        this.$emit("update-review", updatedreview, this.review);
      });
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
      this.comments = this.comments.map((comment) => {
        if (comment === updatedcomment) {
          return updatedcomment;
        } else {
          return comment;
        }
      });
      const idx = this.comments.indexOf(beforecomment);
      this.comments[idx] = updatedcomment;
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
      .then((res) => {
        console.log(this.isLogin);
        this.isLiked = res.data.isLiked;
        this.isDisliked = res.data.isDisliked;
        this.likeCnt = res.data.likeCnt;
        this.dislikeCnt = res.data.dislikeCnt;
        this.commentCnt = res.data.commentCnt;
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
    ...mapGetters(["isLogin", "config"]),
  },
};
</script>

<style>
</style>