<template>
  <div>
    <profile-movie></profile-movie>
    <profile-review></profile-review>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileMovie from '@/components/ProfileMovie.vue'
import ProfileReview from '@/components/ProfileReview.vue'

export default {
  name: 'Profile',
  components: {
    ProfileMovie,
    ProfileReview,
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem("jwt");
      const config = {
        Authorization: `JWT ${token}`,
      };
      return config;
    },
  },
  created: function () {
    axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v2/${this.$route.params.username}/profile/`,
        headers: this.setToken(),
      
      }).then(res => {
        
        console.log(res.data)


      }).catch(err => { console.log(err) })
  }

}
</script>

<style>

</style>