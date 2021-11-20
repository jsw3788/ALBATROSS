<template>
  <div>
    <ul>
      <h3>가장 좋아하는 영화</h3>
      <profile-movie-item
       v-for="movie in favorite_movies"
       :key="movie.id"
       :movie="movie"
      >

      </profile-movie-item>
    </ul>
    <ul>
      <h3>최근 감상 영화</h3>
      <profile-movie-item
       v-for="movie in recent_movies"
       :key="movie.id"
       :movie="movie"
      >

      </profile-movie-item>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileMovieItem from '@/components/ProfileMovieItem'
import { mapState } from 'vuex'

export default {
  name: 'ProfileMovie',
  components: {
    ProfileMovieItem
  },
  data: function () {
    return {
      // 이 두 리스트는 형태가 같아야함
      favorite_movies: null,
      recent_movies: null,
    }
  },
  created: function() {
    axios({
        method: 'get',
        
        url: `http://127.0.0.1:8000/api/v1/${this.username}/movies/favorite/`,
        // headers: this.setToken(),
      
      }).then(res => {
        // console.log('favorite_movies')
        // console.log(res)
        this.favorite_movies = res.data

      }).catch(err => { console.log(err) })


      axios({
        method: 'get',
        
        url: `http://127.0.0.1:8000/api/v1/${this.username}/movies/recent/`,
        // headers: this.setToken(),
      
      }).then(res => {
        // console.log('recent_movies')
        // console.log(res)
        this.recent_movies = res.data


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