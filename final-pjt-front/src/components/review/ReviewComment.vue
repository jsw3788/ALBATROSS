<template>
  <div v-if="!comment.is_spoiled">
    <div class="d-flex align-items-center">
      <div class="my-2 mx-2">
        <b-icon-arrow-return-right></b-icon-arrow-return-right>
        {{ comment.user.username }} : {{ comment.content }} |

        <span>
          {{ humanize(new Date(), comment.updated_at) }}
          <span
            v-if="
              humanize(new Date(), comment.created_at) !== '지금' &&
              comment.created_at !== comment.updated_at
            "
            >(수정됨)</span
          >
        </span>
      </div>
      <div>
        <span v-if="comment.user.username === this.username">
          <b-icon-pencil-fill
            v-b-modal="'update' + comment.id"
            size="sm"
            class="mx-1"
          ></b-icon-pencil-fill>

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
          <b-icon-trash
            @click="deleteComment"
            size="sm"
            class="mx-1"
          ></b-icon-trash>
        </span>
      </div>
    </div>
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
      }).catch((err) =>
      console.log(err));
    },
    deleteComment: function () {
      const delComment = this.comment;
      axios({
        method: "delete",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/comments/${this.comment.id}/`,
        headers: this.$store.getters.config,
      }).then(() => {
        this.$emit("delete-comment", delComment);
      }).catch((err) => console.log(err));
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