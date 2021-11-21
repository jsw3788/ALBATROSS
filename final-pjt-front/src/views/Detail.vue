<template>
  <div id="detail">
    <div>
      <b-img :src="movie.backdrop_path" fluid :alt="movie.poster_path"></b-img>
    </div>
    <b-container class="bv-example-row">
      <b-row class="text-center">
        <b-col cols="3">
          <div>
            <div>
              <b-card
                :title="movie.title"
                :img-src="movie.poster_path"
                img-alt="Poster"
                img-top
                tag="article"
                class="mb-2 side-card"
              >
                <b-card-text>
                  <p>{{ movie.release_date }}</p>
                  <p v-if="movie.tmdb_vote_cnt">
                    평점: {{ movie.tmdb_vote_sum / movie.tmdb_vote_cnt / 2 }}
                  </p>
                  <p v-else>등록된 평점이 없습니다.</p>
                  <!-- <star-rating :increment="0.5"></star-rating> -->
                  <div
                    @click="showCurrentRating(0)"
                    @mouseleave="showCurrentRating(0)"
                    style="display: inline-block"
                  >
                    <star-rating
                      :show-rating="false"
                      @current-rating="showCurrentRating"
                      @rating-selected="setCurrentSelectedRating"
                      :increment="0.5"
                    ></star-rating>
                  </div>
                  <div style="margin-top: 10px; font-weight: bold">
                    {{ currentRating }}
                  </div>
                  <p>
                    <span v-for="genre in movie.genres" :key="genre.id"
                      >{{ genre.name }}
                    </span>
                  </p>
                </b-card-text>
              </b-card>
            </div>
          </div>
        </b-col>
        <b-col cols="9">
          <div>
            <p>줄거리</p>
            <p>{{ movie.overview }}</p>
          </div>
          <div>
            <review-form
              :movieId="movie.id"
              @add-review="addReview"
            ></review-form>
            <review-list
              v-for="review in reviews"
              :key="review.id"
              :review="review"
              :movieId="movie.id"
              @delete-review="deleteReview"
            ></review-list>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <div></div>
    <div></div>
    <div v-if="isLogin">
      <button v-if="wanted" @click="updatedWanted">보고싶어요 취소</button>
      <button v-else @click="updatedWanted">보고싶어요</button>
    </div>
  </div>
</template>

<script>
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

      rating: "No Rating Selected",
      currentRating: "별점을 매겨주세요",
      currentSelectedRating: "",
      // boundRating: 3,
    };
  },
  methods: {
    updatedWanted: function () {
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/wanted/${this.$route.params.movie_id}/`,
        headers: this.config,
      })
        .then((res) => {
          console.log(res);
          this.wanted = res.data.wanted;
        })
        .catch((err) => {
          console.log(err);
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
    checkScore: function () {
      // score 데이터 가져오기
      axios({
            method: "get",
            url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
            headers: this.$store.getters.config,
            
        }).then((res) => {
          // console.log(res)
          const tempscore = res.data.score
          console.log("tempscore:"+tempscore)
          if (tempscore === 0){
            this.currentRating = "별점을 매겨주세요"
          }else{
            this.currentRating = "평가함 ☆: " + tempscore 
          }
          this.showCurrentRating()
          console.log(this.currentRating)
            
          })
          .catch((err) => {
            console.log(err);
          })
    },

    addReview: function (review) {
      this.reviews.push(review);
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
    setCurrentSelectedRating: function (score) {
      // 평가한 데이터가 없으면 생성
      console.log(this.currentSelectedRating)
      if (!this.currentSelectedRating){
        axios({
          method: "post",
          url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
          headers: this.$store.getters.config,
          data: {
            score: score,
          }
      }).then((res) => {
        
          this.wanted=res.data.wanted
        })
        .catch((err) => {
          console.log(err);
        })
      } else{
        // 평가한 데이터가 있으면 수정
        axios({
          method: "put",
          url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/score/${this.$route.params.movie_id}/`,
          headers: this.$store.getters.config,
          data: {
            score: score,
          }
      }).then((res) => {
          this.wanted = res.data.wanted
        })
        .catch((err) => {
          console.log(err);
        })
      }
      this.currentSelectedRating = "평가함 ☆: " + score ;
    },
  },
  computed: {
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
        this.reviews = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
    
      
    if (this.isLogin) {
      this.checkWanted();
      this.checkScore();
      
    }
  },
};
</script>

<style scoped>
#detail {
  color: white;
}
.side-card {
  background-color: black;
}
</style>