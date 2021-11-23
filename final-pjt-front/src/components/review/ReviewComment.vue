<template>
  <div v-if="!comment.is_spoiled">
    <p>
      댓글 // {{ comment.user.username }} : {{ comment.content }} |
      {{ humanize(new Date(), comment.created_at) }} |
      {{ humanize(new Date(), comment.updated_at) }}
      <span v-if="comment.user.username === this.username">
        <b-button v-b-modal="'update' + comment.id">수정</b-button>

        <b-modal
          title="댓글 수정"
          :id="'update' + comment.id"
          ok-only
          hide-footer
        >
          <template #default="{ close }">
            <input
              type="text"
              v-model.trim="updatedcontent"
              @keyup.enter="updateComment"
            />
            <b-button @click="[updateComment(), close()]">수정</b-button>
          </template>
        </b-modal>
        <b-button @click="deleteComment">삭제</b-button>
      </span>
    </p>
  </div>
  <div v-else>
    <div>
      <p>이 댓글은 스포일러를 담고 있습니다.</p>
      <p>
        내용을 보시려면 <b-button @click="lookspoiler">여기</b-button>를
        클릭해주세요.
      </p>
    </div>
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
    return {
      updatedcontent: this.comment.content,
    };
  },
  methods: {
    updateComment: function () {
      axios({
        method: "put",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/comments/${this.comment.id}/`,
        headers: this.$store.getters.config,
        data: {
          content: this.updatedcontent,
        },
      }).then(() => {
        const updatedcomment = {
          ...this.comment,
          content: this.updatedcontent,
        };
        this.$emit("update-comment", updatedcomment, this.comment);
      });
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
      this.comment.is_spoiled = false;
    },
  },
  computed: {
    ...mapState(["username"]),
  },
};
</script>

<style>
</style>