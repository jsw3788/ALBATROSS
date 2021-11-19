<template>
  <div>
    <li>
      <img :src="image">
      <p>
      {{ name }}
      </p>
      <p>
      {{ popularity }}
      </p>
      <p>연출작들</p>
      <span
        v-for="movie in movies"
          :key="movie.poster_path"
      >

        <img :src="movie.poster_path">
        <p>{{ movie.title }}</p>
      
      </span>

    </li>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PeopleDirectorDetail',
  data: function () {
    return {
      name: null,
      movies: null,
      image: null,
      popularity: null,

    }
  },
  created: function () {
    axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/people/directors/${this.$route.params.director_pk}`,
      }).then(res =>{
        this.name = res.data.name
        this.movies = res.data.movies
        this.popularity = res.data.popularity
        this.image = res.data.profile_path

      }).catch(err => {console.log(err)})
  }
}
</script>

<style>

</style>