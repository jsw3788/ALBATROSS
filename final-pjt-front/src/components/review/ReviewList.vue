<template>
  <div id="review-list">
    <!-- 리뷰 하나당 대댓글이 다 달려야함 -->
    <!-- 댓글 -->
    <div v-if="!review.is_spoiled">
      <div class="py-3 px-5">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <div class="text-start">
            <span
              ><img
                :src="image"
                alt="profile"
                style="width: 20%; border-radius: 50%"
                class="me-2"
            /></span>
            <span @click="goProfile">{{ review.user.username }}</span>
          </div>
          <div class="d-flex">
            <div class="me-3">
              <span>
                {{ humanize(new Date(), review.updated_at) }}
              </span>
              <span
                v-if="
                  humanize(new Date(), review.created_at) !== '지금' &&
                  review.created_at !== review.updated_at
                "
                >(수정됨)</span
              >
            </div>
            <!-- 수정, 삭제 -->
            <div v-if="review.user.username === this.username">
              <b-icon-pencil-fill
                v-b-modal="'update' + review.id"
                size="sm"
                class="me-2"
              ></b-icon-pencil-fill>
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
              <b-icon-trash
                @click="deleteReview"
                size="sm"
                class="me-2"
              ></b-icon-trash>
            </div>
          </div>
        </div>
        <div>
          <p class="text-start">{{ review.content }}</p>
        </div>
      </div>
      <div class="d-flex justify-content-between px-5">
        <div class="text-start ms-3">{{ commentCnt }}개의 댓글이 있습니다</div>
        <div class="d-flex align-items-start justify-content-end me-3">
          <!-- 공감, 비공감 -->
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
        </div>
      </div>
      <!-- comment -->
      <b-container class="bv-example-row px-5">
        <b-row>
          <b-col cols="1"></b-col>
          <b-col cols="11 border-start border-3">
            <!-- comment list -->
            <div>
              <review-comment
                v-for="comment in comments"
                :key="comment.id"
                :comment="comment"
                @update-comment="updateComment"
                @delete-comment="deleteComment"
              ></review-comment>
            </div>
            <!-- comment form -->
            <div class="text-end my-2" v-if="letWrite">
              <div class="text-start">
                <button @click="clickWrite">접기</button>
              </div>
              <input
                type="text"
                v-model.trim="newComment"
                @keyup.enter="writeComment"
                class="mx-2"
                style="width: 100%"
              />
              <input
                type="checkbox"
                :id="'comment-spoil' + review.id"
                v-model="newCommentSpoil"
              />
              <label :for="'comment-spoil' + review.id" class="mx-1"
                >spoiler</label
              >
              <b-icon-pencil-square
                @click="writeComment"
              ></b-icon-pencil-square>
            </div>
            <div v-else class="text-start">
              <button @click="clickWrite">댓글 쓰기</button>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div v-else>
      <div>
        <p>이 글은 스포일러를 담고 있습니다.</p>
        <p>
          내용을 보시려면 <b-button @click="lookspoiler">여기</b-button>를
          클릭해주세요.
        </p>
      </div>
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
      letWrite: false,
      image:
        `${process.env.VUE_APP_SERVER_URL}` + this.review.user.profile_image,
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
      })
        .then(() => {
          const updatedreview = {
            ...this.review,
            content: this.updatedcontent,
          };
          this.$emit("update-review", updatedreview, this.review);
        })
        .catch((err) => console.log(err));
    },
    deleteReview: function () {
      console.log(this.username);
      const delReview = this.review;
      axios({
        method: "delete",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/`,
        headers: this.$store.getters.config,
      })
        .then(() => {
          this.$emit("delete-review", delReview);
        })
        .catch((err) => console.log(err));
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
          this.commentCnt += 1;
          this.newCommentSpoil = false;
        })
        .catch(() => {
          Vue.notify({
            group: "review_notify",
            title: "멈춰!",
            text: "댓글 작성을 위해 로그인이 필요합니다.",
            type: "warn",
            closeOnClick: true,
          });
        });
    },
    clickWrite: function () {
      this.letWrite = !this.letWrite;
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
      this.commentCnt -= 1;
    },
    humanize: function (now, date) {
      const moment = require("moment");
      const getTime = new Date(date);
      let temp = parseInt(now - getTime); // ms단위로, 3일-24시간-60분-지금
      if (259200000 < temp) {
        temp = moment(getTime).format(""); // 3일보다 오래 지났으면 날짜로 반환
      } else if (86400000 < temp) {
        temp = parseInt(temp / 86400000).toString() + "일 전";
      } else if (3600000 < temp) {
        temp = parseInt(temp / 3600000).toString() + "시간 전";
      } else if (60000 < temp) {
        temp = parseInt(temp / 60000).toString() + "분 전";
      } else {
        temp = "지금";
      }
      return temp;
    },
    lookspoiler: function () {
      this.review.is_spoiled = false;
    },
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/reviews/${this.review.id}/`,
      headers: this.$store.getters.config,
    })
      .then((res) => {
        // console.log(this.isLogin);
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