<template>
  <div id="detail">
    <div class="backdrop-box">
      <b-img
        :src="movie.backdrop_path"
        fluid
        :alt="movie.poster_path"
        class="backdrop"
      ></b-img>
    </div>
    <b-container class="bv-example-row">
      <b-row class="text-center">
        <b-col cols="3">
          <div class="card-box">
            <b-card
              :title="movie.title"
              :img-src="movie.poster_path"
              img-alt="Poster"
              img-top
              tag="article"
              class="mt-5 side-card"
            >
              <b-card-text>
                <div>
                  <p>{{ movie.release_date }}</p>
                  <p v-if="movie.tmdb_vote_cnt">평점 : {{ movieRate }}</p>
                  <p v-else>등록된 평점이 없습니다.</p>
                </div>
                <div v-if="isLogin">
                  <div class="d-flex justify-content-evenly">
                    <div></div>
                    <div>
                      <i
                        class="fas fa-heart"
                        v-if="wanted"
                        @click="updatedWanted"
                        style="color: rgb(237, 73, 86)"
                      ></i>
                      <i
                        class="far fa-heart"
                        v-else
                        @click="updatedWanted"
                        style="color: rgb(237, 73, 86)"
                      ></i>
                    </div>
                    <div v-if="isScored" @click="deleteScore">
                      <b-icon-eye-slash-fill></b-icon-eye-slash-fill>
                    </div>
                    <div></div>
                  </div>
                  <div
                    @click="showCurrentRating(0)"
                    @mouseleave="showCurrentRating(0)"
                    style="display: inline-block"
                    class="my-2"
                  >
                    <star-rating
                      :star-size="30"
                      :rating="score"
                      :rounded-corners="true"
                      :show-rating="false"
                      @current-rating="showCurrentRating(score)"
                      @rating-selected="setCurrentSelectedRating"
                      :increment="0.5"
                    ></star-rating>
                  </div>
                  <div style="margin-top: 10px; font-weight: bold">
                    {{ currentRating }}
                  </div>
                </div>
                <p>
                  <span v-for="genre in movie.genres" :key="genre.id"
                    >{{ genre.name }}
                  </span>
                </p>
              </b-card-text>
            </b-card>
          </div>
        </b-col>
        <b-col cols="9">
          <div class="text-start">
            <p class="m-3">줄거리</p>
            <p class="m-3">{{ movie.overview }}</p>
          </div>
          <!-- 이하 리뷰칸 -->
          <div class="review">
            <review-form
              :movieId="movie.id"
              @add-review="addReview"
            ></review-form>
            <hr />
            <review-list
              v-for="review in reviews"
              :key="review.id"
              :review="review"
              :movieId="movie.id"
              @update-review="updateReview"
              @delete-review="deleteReview"
            ></review-list>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div></div>
    <div></div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import ReviewForm from "@/components/review/ReviewForm";
import ReviewList from "@/components/review/ReviewList";
import { mapGetters } from "vuex";

export default {
  name: "Detail",
  components: {
    ReviewForm,
    ReviewList,
  },
  data: function () {
    return {
      movie: "",
      reviews: "",
      wanted: null,
      score: null,
      movieRate: null,
      pageNum: 2,
      possiblePageNum:1,
      // loading: 2,
      loadingCheck: true,


      rating: "No Rating Selected",
      currentRating: "평점을 매겨주세요",
      currentSelectedRating: "",
    };
  },
  methods: {
    // 인피니티 스크롤
    getMoreReviews: function () {
      axios({

            method: 'get',
            url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/${this.movie.id}/reviews/`,
            headers: this.$store.getters.config,
            params: {
              page: this.pageNum,
            },
          })
          .then((res) =>{
            
            this.possiblePageNum = res.data.pop()['last_page']
            
            const newreviews = res.data
            this.reviews.push(...newreviews)
            this.pageNum += 1
            this.loadingCheck=true
          }).catch((err)=>
          console.log(err))

    },
    scrollDown: function () {
      const { scrollHeight, scrollTop, clientHeight} = document.documentElement
        if (scrollHeight - Math.round(scrollTop) <= clientHeight) {
          if (this.pageNum <= this.possiblePageNum && this.possiblePageNum != 1) {
            if(this.loadingCheck){
            // if(this.loading == this.pageNum){
              this.getMoreReviews()
              // this.loading+=1
              this.loadingCheck=false
            }
          } 

        }
      },
    updatedWanted: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/wanted/${this.$route.params.movie_id}/`,
        headers: this.config,
      })
        .then((res) => {
          this.wanted = res.data.wanted;
        })
        .catch(() => {
          Vue.notify({
            group: "movie_notify",
            title: "앗!",
            text: "이미 시청한 영화입니다! 시청하지 않았다면, 평점을 취소해주세요!",
            type: "warn",
          });
        });
    },
    checkWanted: function () {
      axios({
        method: "get",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/wanted/${this.$route.params.movie_id}/`,
        headers: this.config,
      })
        .then((res) => {
          this.wanted = res.data.wanted;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    addReview: function (review) {
      // console.log(review);
      this.reviews.push(review);
    },
    updateReview: function (updatedreview, beforereview) {
      this.reviews = this.reviews.map((review) => {
        if (review === updatedreview) {
          return updatedreview;
        } else {
          return review;
        }
      });
      const idx = this.reviews.indexOf(beforereview);
      this.reviews[idx] = updatedreview;
    },
    deleteReview: function (delReview) {
      const idx = this.reviews.indexOf(delReview);
      this.reviews.splice(idx, 1);
    },

    setRating: function (rating) {
      this.rating = "Selected: " + rating + " stars";
    },
    showCurrentRating: function (rating) {
      this.currentRating = rating === 0 ? this.currentSelectedRating : "";
    },
    checkScore: function () {
      // score 데이터 가져오기
      axios({
        method: "get",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
        headers: this.$store.getters.config,
      })
        .then((res) => {
          // console.log(res)
          const tempscore = res.data.score;

          if (tempscore === 0) {
            this.currentRating = "평점을 매겨주세요";
          } else {
            this.showCurrentRating(0);
            this.currentRating = "평가함 ★ " + tempscore;
          }
          this.score = tempscore;
          // console.log(this.score);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    setCurrentSelectedRating: function (score) {
      // 평가한 데이터가 없으면 생성
      if (!this.score) {
        axios({
          method: "post",
          url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
          headers: this.$store.getters.config,
          data: {
            score: score,
          },
        })
          .then((res) => {
            this.wanted = res.data.wanted;
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        // 평가한 데이터가 있으면 수정
        axios({
          method: "put",
          url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
          headers: this.$store.getters.config,
          data: {
            score: score,
          },
        })
          .then((res) => {
            this.wanted = res.data.wanted;
          })
          .catch((err) => {
            console.log(err);
          });
      }
      this.currentSelectedRating = "평가함 ☆: " + score;
      this.score = score;
    },
    deleteScore: function () {
      axios({
        method: "delete",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
        headers: this.$store.getters.config,
        data: {
          delScore: this.score,
        },
      })
        .then(() => {
          this.score = 0;
          this.currentSelectedRating = "";
          this.showCurrentRating(0);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },

  computed: {
    isScored: function () {
      return this.score;
    },
    ...mapGetters(["isLogin", "config"]),
  },
  created: function () {
    // 영화 디테일 가져오기
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/detail/${this.$route.params.movie_id}`,
      // headers: this.$store.getters.config,
    })
      .then((res) => {
        // console.log(res);
        this.movie = res.data;
        // console.log(this.movie);
        if (this.movie.updated_vote_cnt + this.movie.tmdb_vote_cnt) {
          this.movieRate =
            (this.movie.tmdb_vote_sum + this.movie.updated_vote_sum) /
            (this.movie.tmdb_vote_cnt + this.movie.updated_vote_cnt) /
            2;
          this.movieRate = this.movieRate.toFixed(2);
        }
      })
      .then({})
      .catch((err) => {
        console.log(err);
      });

    // 영화에 달린 리뷰 가져오기
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/${this.$route.params.movie_id}/reviews/`,
      headers: this.$store.getters.config,
    })
      .then((res) => {
        this.possiblePageNum=res.data.pop()['last_page']
        this.reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });

    if (this.isLogin) {
      this.checkWanted();
      this.checkScore();
    }

    setTimeout(() =>{
      document.addEventListener('scroll', this.scrollDown)
    }, 2000)
  },
  destroyed: function () {
    document.removeEventListener("scroll", this.scrollDown);
  },
};
</script>

<style scoped>
.side-card {
  background-color: #301b3f;
}
.review {
  background-color: #301b3f;
}
.backdrop-box {
  max-height: 15rem;
  overflow: hidden;
  margin-bottom: 1rem;
}
.backdrop {
  /* max-height: initial;
  filter: blur(5px);
  -webkit-filter: blur(5px);
  -moz-filter: blur(5px);
  -o-filter: blur(5px);
  -ms-filter: blur(5px); */
}
</style>