<template>
  <div>
    <ul>
      <profile-review-item
       v-for="review in popular_reviews"
       :key="review.id"
       :review="review"
      >

      </profile-review-item>
    </ul>
    <ul>
      <profile-movie-item
       v-for="review in recent_reviews"
       :key="review.id"
       :review="review"
      >

      </profile-movie-item>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileReviewItem from '@/components/ProfileReviewItem'
import { mapState } from 'vuex'

export default {
name: 'ProfileReview',
  components: {
    ProfileReviewItem
  },
  data: function () {
    return {
      // 이 두 리스트는 형태가 같아야함
      popular_reviews: null,
      recent_reviews: null,
    }
  },
  created: function() {
    axios({
        method: 'get',
        
        url: `http://127.0.0.1:8000/api/v1/${this.username}/reviews/popular/`,
        // headers: this.setToken(),
      
      }).then(res => {
        
        console.log(res)
        // this.favorite_movies = 

      }).catch(err => { console.log(err) })


      axios({
        method: 'get',
        
        url: `http://127.0.0.1:8000/api/v1/${this.username}/reviews/recent/`,
        // headers: this.setToken(),
      
      }).then(res => {
        
        console.log(res)
        // this.recent_movies = 


      }).catch(err => { console.log(err) })
  },
  computed: {
    ...mapState([
      'username'
    ])
  }
}
</script>

<style>

</style>